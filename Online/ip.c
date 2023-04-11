#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <unistd.h>
#include <arpa/inet.h>
#include <ifaddrs.h>
#include <net/if.h>
#include "ip.h"

int rm(char *path)
{
	if(unlink(path) == -1)
		return -1;
	return 0;
}

int cp(char *src, char *dest)
{
	FILE *file_src = fopen(src,"r");
	FILE *file_dest = fopen(dest,"w");

	char c;

	if(file_src != NULL && file_dest != NULL)
	{
		while((c = fgetc(file_src)) != EOF)
		{	
			fputc(c, file_dest);
		}
	}
	else{
		return -1;
	}

	fclose(file_src);
	fclose(file_dest);

	return 0;
}

int inserer_ip(char *path, char *ip)
{
	if(strlen(ip) > 15)
	{
		perror("\nAdresse IP incorrecte\n");
		return -1;
	}
	FILE *file = fopen(path, "a+"); 
	if(file == NULL)
	{
		perror("\nErreur dans l'ouverture fichier\n");
		return -1;
	}

	if(fwrite(ip, 1, strlen(ip), file) != strlen(ip))
	{
		perror("\nErreur dans l'ecriture dans le fichier\n");
		return -1;
	}

	if(fputc('\n', file) != 10)
	{
		perror("\nErreur dans l'ecriture dans le fichier\n");
		return -1;
	}

	fclose(file);
	return 0;
}

int enlever_ip(char *path, char *ip)
{
	if(strlen(ip) > 15)
	{
		perror("\nAdresse IP incorrecte\n");
		return -1;
	}

	FILE *file = fopen(path, "a+");
	FILE *ftemp = fopen("file_temp", "w+");

	if(file == NULL || ftemp == NULL)
	{
		perror("\nErreur dans l'ouverture fichier\n");
		return -1;
	}

	fseek(file,0, SEEK_SET);
	char *read_buffer = calloc(1, 16);
	char c;
	int i=0;

	while((c=fgetc(file)) != EOF)
	{
		if(c == '\n'){
			i = 0;
			if(strcmp(read_buffer, ip) != 0)
			{
				if(fwrite(read_buffer, 1, strlen(read_buffer), ftemp) != strlen(read_buffer))
				{
					perror("\nErreur dans l'ecriture dans le fichier temporaire\n");
					return -1;
				}
				if(fputc('\n', ftemp) != 10)
				{
					perror("\nErreur dans l'ecriture dans le fichier temporaire\n");
					return -1;
				}
			}
			bzero(read_buffer, strlen(read_buffer));
			continue;
		}
		read_buffer[i] = c;
		i++;
	}

	fclose(ftemp);
	fclose(file);

	rm(path);
	cp("file_temp", path);
	rm("file_temp");

	return 0;
}

char *get_myIP()
{
	struct ifaddrs *ifaddr, *ifa;
    char *addr;
    
    if (getifaddrs(&ifaddr) == -1) {
        perror("getifaddrs");
        exit(EXIT_FAILURE);
    }
    
    for (ifa = ifaddr; ifa != NULL; ifa = ifa->ifa_next) {
        if (ifa->ifa_addr != NULL && ifa->ifa_flags & IFF_UP && ifa->ifa_addr->sa_family == AF_INET) {
            addr = inet_ntoa(((struct sockaddr_in *)ifa->ifa_addr)->sin_addr);
            
            if(strcmp(addr,"127.0.0.1") != 0) 
				return addr;
        }
    }
    
    freeifaddrs(ifaddr);
    return NULL;
}

int get_nb_lines()
{
	int counter=0;
	char *buffer=calloc(1,250);
	FILE*stream=fopen("addressIP.txt","r");
	if(stream==NULL){
	perror("fopen");
	}
	if(fread(buffer,1,250,stream)<0){
	perror("fread");
	}
	int i=0;
	while(buffer[i]!='\0'){
	if(buffer[i]=='\n'){
	counter++;
	}
	i++;
	}
	return counter;
}

char *firstIP(){
char *buffer=calloc(1,250);
char *firstIp=calloc(1,250);
FILE*stream=fopen("addressIP.txt","r");
 if(stream==NULL){
 perror("fopen");
 }
 if(fread(buffer,1,250,stream)<0){
 perror("fread");
 }
 int i=0;
 while(buffer[i]!='\n'){
 firstIp[i]=buffer[i];
 i++;
 }
 return firstIp;
}

char *get_sender_ip()
{
	FILE *file = fopen("addressIP.txt", "r");

	if(file == NULL)
	{
		perror("\nErreur dans l'ouverture fichier\n");
		return NULL;
	}

	int nb_lines = get_nb_lines();
	int my_nb_line = 0;
	char *myIP = calloc(1,16);
	char *to_sendIP = calloc(1,16);

	myIP = get_myIP();

	fseek(file,0, SEEK_SET);
	char *read_buffer = calloc(1, 16);
	char c;
	int i=0;

	while((c=fgetc(file)) != EOF)
	{
		if(c == '\n'){
			i = 0;
			my_nb_line++;
			if(strcmp(read_buffer, myIP) == 0)
			{
				if(nb_lines <= 1)
				{
					return myIP;
				}
				else if(nb_lines == my_nb_line)
				{
					return firstIP();
				}
				else{
					int j = 0;
					while((c=fgetc(file)) != '\n')
					{
						to_sendIP[j] = c;
						j++;
					}
					return to_sendIP;
				}
			}
			bzero(read_buffer, strlen(read_buffer));
			continue;
		}
		read_buffer[i] = c;
		i++;
	}
}


