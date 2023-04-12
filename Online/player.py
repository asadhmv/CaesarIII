import ctypes, os, subprocess

class Player:


    def __init__(self):

        """os.chdir('Online')
        subprocess.run(["gcc",  "-c", "-fPIC", "ip.c"])
        subprocess.run(["gcc", "-shared", "-fPIC", "-o", "libPlayer.so", "ip.o"])
        os.chdir('..')"""
        self.libPlayer = ctypes.cdll.LoadLibrary('Online/libPlayer.so')
        self.libPlayer.get_myIP.restype = ctypes.c_char_p
        self.ip= self.libPlayer.get_myIP().decode()

    def set_ip(self, ip : str):
        self.ip = ip

    def get_ip(self) -> str:
        return self.ip
    
    def set_username(self, username):
        self.username = username
    
    def get_username(self) -> str:
        return self.username
    
    def get_ip(self):
        return self.ip

