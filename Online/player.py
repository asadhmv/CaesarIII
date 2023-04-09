import ctypes, os, subprocess

class Player:


    def __init__(self,username):

        self.username = username
        self.ip = ""
        os.chdir('Online')
        subprocess.run(["gcc",  "-c", "-fPIC", "ip.c"])
        subprocess.run(["gcc", "-shared", "-fPIC", "-o", "libPlayer.so", "ip.o"])
        os.chdir('..')
        self.libPlayer = ctypes.cdll.LoadLibrary('Online/libPlayer.so')
        self.libPlayer.get_myIP.restype = ctypes.c_char_p
        self.ip= self.libPlayer.get_myIP()

    """def set_ip(self):
        self.ip = "assresse IP"""
    
    def get_ip(self):
        return self.ip
    
    def get_username(self):
        return self.username

