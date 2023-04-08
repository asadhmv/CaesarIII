#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <unistd.h>

#define PORT 1234
#define BUFF_LEN 1024

char * recvC()
{

 int sock = socket(AF_INET, SOCK_DGRAM, 0);
 if (sock == -1) {
 perror("socket");
 exit(EXIT_FAILURE);
 }


 int enable_reuseaddr = 1;
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


 char* buffer=calloc(1,BUFF_LEN);
 struct sockaddr_in sender_addr;
 socklen_t sender_addr_len = sizeof(sender_addr);

 if((res = recvfrom(sock, buffer, BUFF_LEN, 0, (struct sockaddr *)&sender_addr, &sender_addr_len))<0){
 return NULL;
 }


 printf("Received broadcast message from %s:%d: %s\n", inet_ntoa(sender_addr.sin_addr), ntohs(sender_addr.sin_port), buffer);

 close(sock);

 return buffer;
}
