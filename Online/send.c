#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <unistd.h>
#include <ifaddrs.h>
#include <time.h>
#define PORT 1234

char* get_Broadcast() {
    struct ifaddrs *ifaddr, *ifa;
    int family, s;
    char *host=calloc(1,1025);

    if (getifaddrs(&ifaddr) == -1) {
        perror("getifaddrs");
        return NULL;
    }

    // Parcourir les interfaces réseau
    for (ifa = ifaddr; ifa != NULL; ifa = ifa->ifa_next) {
        if (ifa->ifa_addr == NULL)
            continue;

        family = ifa->ifa_addr->sa_family;

        // Obtenir l'adresse de diffusion de l'interface réseau par défaut
        if (family == AF_INET && (ifa->ifa_flags & 0x02)) {
            struct sockaddr_in *addr = (struct sockaddr_in *)ifa->ifa_broadaddr;
            strcpy(host, inet_ntoa(addr->sin_addr));
            return  host;
        }
    }

    freeifaddrs(ifaddr);
    return NULL;
}

void sendC_broadcast(char *arg)
{

    int sock = socket(AF_INET, SOCK_DGRAM, 0);
    if (sock == -1) {
        perror("socket");
        exit(EXIT_FAILURE);
    }


    int enable_broadcast = 1;
    int res = setsockopt(sock, SOL_SOCKET, SO_BROADCAST, &enable_broadcast, sizeof(enable_broadcast));
    if (res == -1) {
        perror("setsockopt");
        exit(EXIT_FAILURE);
    }
   
    struct sockaddr_in broadcast_addr;
    memset(&broadcast_addr, 0, sizeof(broadcast_addr));
    broadcast_addr.sin_family = AF_INET;
    broadcast_addr.sin_port = htons(PORT);
    broadcast_addr.sin_addr.s_addr = inet_addr(get_Broadcast());


    res = sendto(sock, arg, 1024, 0, (struct sockaddr *)&broadcast_addr, sizeof(broadcast_addr));
    if (res == -1) {
        perror("sendto");
        exit(EXIT_FAILURE);
    }

    close(sock);

}

void sendC(char *message, char *adresse_ip)
{
    struct sockaddr_in sockaddr;
	int sockfd=-1, slen=sizeof(sockaddr);

	if( (sockfd=socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP)) == -1)
	{
		perror("socket() :");
        exit(EXIT_FAILURE);
	}

	memset((char *) &sockaddr, 0, sizeof(sockaddr));
	sockaddr.sin_family = AF_INET;
	sockaddr.sin_port = htons(PORT);
	
	if(inet_aton(adresse_ip , &sockaddr.sin_addr) == 0) 
	{
        perror("inet_aton() failed : ");
        exit(EXIT_FAILURE);
	}
    if(sendto(sockfd, message, strlen(message) , 0 , (struct sockaddr *) &sockaddr, slen)==-1)
    {
        perror("sendto() :");
        exit(EXIT_FAILURE);
    }

	close(sockfd);
}

