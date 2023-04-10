#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <unistd.h>
#include <errno.h>
#define PORT 1234
#define BUFF_LEN 1024

char ** recvC(int sock)
{
    int enable_reuseaddr = 1;
    struct timeval timeout;
    timeout.tv_sec = 1;  // délai d'attente de 1 secondes
    timeout.tv_usec = 0;

    // configuration du délai d'attente sur la socket
    if (setsockopt(sock, SOL_SOCKET, SO_RCVTIMEO, &timeout, sizeof(timeout)) == -1) {
        perror("setsockopt");
        exit(1);
    }
    int res = setsockopt(sock, SOL_SOCKET, SO_REUSEADDR, &enable_reuseaddr, sizeof(enable_reuseaddr));
    if (res == -1) {
        perror("setsockopt");
        exit(EXIT_FAILURE);
    }


    struct sockaddr_in listen_addr;
    memset(&listen_addr, 0, sizeof(listen_addr));
    listen_addr.sin_family = AF_INET;
    listen_addr.sin_port = htons(PORT);
    listen_addr.sin_addr.s_addr = INADDR_ANY;


    res = bind(sock, (struct sockaddr *)&listen_addr, sizeof(listen_addr));
    if (res == -1) {
        perror("bind");
        exit(EXIT_FAILURE);
    }

    struct sockaddr_in sender_addr;
    socklen_t sender_addr_len = sizeof(sender_addr);

    char* buffer=calloc(1,BUFF_LEN);
    int res_recv;

    if((res_recv = recvfrom(sock, buffer, BUFF_LEN, 0, (struct sockaddr *)&sender_addr, &sender_addr_len))<0){
         if (errno == EAGAIN || errno == EWOULDBLOCK) {
                return NULL;
            } else {
                return NULL;
            }
    }


    char** info=calloc(sizeof(char*),2);
    for (int i=0;i<2;i++){
        info[i]=calloc(1,1024);
    }
    strcpy(info[0],inet_ntoa(sender_addr.sin_addr));
    strcpy(info[1],buffer);

    printf("Received message : '%s'\n",buffer);

    return info;
}

int createSocket()
{
    int sock = socket(AF_INET, SOCK_DGRAM, 0);
    if (sock == -1) {
        perror("socket");
        exit(EXIT_FAILURE);
    }

    return sock;
}

void closeSocket(int sock)
{
    if(sock != -1)
        close(sock);
}
