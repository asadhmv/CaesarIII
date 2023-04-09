import socket 
from menu import Menu


# créer une instance de la classe Menu


class player:
    def __init__(self,username):
        
        self.username=username
        self.ip=""
   

    
    def set_ip(self):
         hostname = socket.gethostname()
         ip = socket.gethostbyname(hostname)
         self.ip = ip



    