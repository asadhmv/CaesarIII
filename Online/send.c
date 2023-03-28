#include<stdio.h>	
#include<string.h> 
#include<stdlib.h> 
#include <unistd.h>
#include<arpa/inet.h>
#include<sys/socket.h>
#include "ip.h"

#define BUFLEN 512	    //Buffer length
#define PORT   1234	    //Destination port



void stop(char *s)
{
	perror(s);
	exit(1);
}

int main()
{
	//------------------------------------PIPE----------------------------------------------------
	const char *pipe_name = "send_pipe";
	int pipe_fd;
	char *buffer = calloc(1,1024);
	pipe_fd = open(pipe_name, O_RDONLY);
	read(pipe_fd, buffer, sizeof(buffer));
	//printf("Message received in C: %s\n", buffer);
	close(pipe_fd);
	//--------------------------------------------------------------------------------------------


	struct sockaddr_in sockaddr;
	int sockfd=-1, slen=sizeof(sockaddr);
	char message[BUFLEN+1];

	char *serverIP = calloc(1,16);
	strcpy(serverIP, get_sender_ip());

	if ( (sockfd=socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP)) == -1)
	{
		stop("socket");
	}

	memset((char *) &sockaddr, 0, sizeof(sockaddr));
	sockaddr.sin_family = AF_INET;
	sockaddr.sin_port = htons(PORT);
	
	if (inet_aton(serverIP , &sockaddr.sin_addr) == 0) 
	{
		fprintf(stderr, "inet_aton() failed\n");
		exit(1);
	}
	//send the message
	
	if (sendto(sockfd, buffer, strlen(buffer) , 0 , (struct sockaddr *) &sockaddr, slen)==-1)
	{
		stop("sendto()");
	}
		
	close(sockfd);
	return 0;
}
