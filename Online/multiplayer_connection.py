import os
import subprocess
import ctypes
import threading
from class_types.buildind_types import BuildingTypes
from class_types.road_types import RoadTypes

list=[]
class Multiplayer_connection:

    def __init__(self, online=False):
        self.list_receive = []
        self.buffer_send = ""
        self.builder = None
        self.online = online
        self.buffer_receive = None
        os.chdir('Online')
        subprocess.run(["gcc",  "-c", "-fPIC", "recv.c"])
        subprocess.run(["gcc",  "-c", "-fPIC", "send.c"])
        subprocess.run(["gcc", "-shared", "-fPIC", "-o", "libNetwork.so", "recv.o", "send.o"])
        os.chdir('..')
        self.libNetwork = ctypes.cdll.LoadLibrary('Online/libNetwork.so')
        self.libNetwork.recvC.restype = ctypes.POINTER(ctypes.c_char_p)
        self.libNetwork.sendC.argtypes = [ctypes.c_char_p]
        self.sock = None
        self.thread_stop_event = threading.Event()
        self.thread = threading.Thread(target=self.receive_thread)
        self.thread.start()
        self.thread2=None


    def set_builder(self, builder):
        self.builder = builder


    def set_buffer_send(self, buffer):
        self.buffer_send = buffer


    
    def write(self, row, col, buildingType="destroy"):
        if not self.online:
            return
        string = str(buildingType) + ";" + str(row) + ";" + str(col)
        self.buffer_send += string
        self.thread2 = threading.Thread(target=self.send, args=(self.buffer_send,))
        self.thread2.start()
        self.set_buffer_send("")


    
    def read(self):
        if not self.online:
            return

        tab = self.list_receive[1].split(";")
        type_str = tab[0]
        type_parts = type_str.split('.')
        type_name = type_parts[-1]

        if "RoadTypes" in type_str:
            type_value = getattr(RoadTypes, type_name)
        elif "BuildingTypes" in type_str:
            type_value = getattr(BuildingTypes, type_name)
        else:
            return

        self.builder.build_from_start_to_end(type_value, Multiplayer_connection.string_to_tuple(tab[1]), Multiplayer_connection.string_to_tuple(tab[2]))


    
    def send(self,buffer):
        if not self.online:
            return
        
        self.libNetwork.sendC(buffer.encode())

    """def receive(self,buffer):
        if len(buffer) > 0:
            self.buffer_receive = buffer.decode()
            self.read()"""

    def receive_thread(self):
        if not self.online:
            return
        while not self.thread_stop_event.is_set():
            self.list_receive=[]
            self.sock = self.libNetwork.createSocket()
            buffer = self.libNetwork.recvC(self.sock)
            if buffer :
                if buffer[0]:
                    self.list_receive.append(buffer[0].decode('utf-8'))
                if buffer[1]:
                    self.list_receive.append(buffer[1].decode('utf-8'))
                self.read()
            self.libNetwork.closeSocket(self.sock)
            
    def kill_thread(self):
        self.thread_stop_event.set()
        self.thread.join()

    def string_to_tuple(string):
        string = string.replace("(", "")
        string = string.replace(")", "")
        string = string.replace(" ", "")

        tab = string.split(",")

        return (int(tab[0]), int(tab[1]))
    



