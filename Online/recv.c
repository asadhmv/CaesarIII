#include <stdio.h>	
#include <string.h> 
#include <stdlib.h> 
#include <unistd.h>
#include <arpa/inet.h>
#include <sys/socket.h>
#include <net/if.h>
#include <ifaddrs.h>
#include <sys/ioctl.h>
#include "ip.h"
#define BUFLEN 512	    //Buffer length
#define PORT   1234	    //Destination port

#define P1 "PONG"

void stop(char *s)
{
	perror(s);
	exit(EXIT_FAILURE);
}

int main(void)
{
	char **arg=calloc(sizeof(char *),3);
	
	arg[0]="./send";
	arg[1]=calloc(1,250);
	arg[2]=NULL;
	
	struct sockaddr_in servaddr, cliaddr;
	int sockfd, len, nbbytes;

	char message[BUFLEN+1];
	char message2[BUFLEN+1];
	bzero(message2,sizeof(message2));

	if ( (sockfd=socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP)) == -1)
	{
		stop("socket");
	}

	memset((char *) &servaddr, 0, sizeof(servaddr));
	servaddr.sin_family = AF_INET;
	servaddr.sin_port = htons(PORT);
	
	
	if (inet_aton(get_myIP() , &servaddr.sin_addr) == 0) 
	{
		fprintf(stderr, "inet_aton() failed\n");
		exit(1);
	}


	// Bind the socket with the server address 
	if ( bind(sockfd, (const struct sockaddr *)&servaddr,  
				sizeof(servaddr)) < 0 ) 
	{ 
		perror("bind failed"); 
		exit(EXIT_FAILURE); 
	} 

        
	for(;;){
		memset(&cliaddr, 0, sizeof(cliaddr)); 
		bzero(&message,BUFLEN+1);
		len=sizeof(cliaddr);
		// recv the message
		if ( (nbbytes = recvfrom(sockfd, message, BUFLEN , 0 , (struct sockaddr *) &cliaddr, (socklen_t *)&len)) < 0)
		{
			stop("recvfrom()");
		}
		if(strncmp(message,message2,strlen(message))!=0){
			const char *pipe_name= "receive_pipe";
			int pipe_fd;
			char *buffer = calloc(1, BUFLEN);

			pipe_fd = open(pipe_name, O_WRONLY);
			write(pipe_fd, message, strlen(message)+1);
			close(pipe_fd);
			

			bzero(arg[1],sizeof(arg[1]));
			strcpy(arg[1],message);
			int pid=fork();
			if(pid==0){
				execvp("./send",arg);
			}			
		}
		for(int i=0;i<strlen(message);i++){
			message2[i]=message[i];
		}


		
	}

	close(sockfd);
	return EXIT_SUCCESS;
}
