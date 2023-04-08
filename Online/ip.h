#ifndef IP_H
#define IP_H

int rm(char *path);
int cp(char *src, char *dest);
int inserer_ip(char *path, char *ip);
int enlever_ip(char *path, char *ip);
char *get_myIP();
char *get_sender_ip();
int get_nb_lines();
char *firstIP();


#endif