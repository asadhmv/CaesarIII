import os
import subprocess
import ctypes
import threading
from class_types.buildind_types import BuildingTypes
from class_types.road_types import RoadTypes
from components.Chat import Chat
list=[]
class Multiplayer_connection:
    instance=None
    def __init__(self, online=True):
        self.buffer_receive = ""
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
        self.libNetwork.recvC.restype = ctypes.c_char_p
        self.libNetwork.sendC.argtypes = [ctypes.c_char_p]
        self.sock = None
        self.thread_stop_event = threading.Event()
        self.thread = threading.Thread(target=self.receive_thread)
        self.thread.start()


    def set_builder(self, builder):
        self.builder = builder


    def set_buffer_send(self, buffer):
        self.buffer_send = buffer
        return
    def set_buffer_receive(self, buffer):
        self.buffer_receive = buffer
        return
    
    def write(self, row, col, buildingType="destroy"):
        if not self.online:
            return
        
        string = str(buildingType) + ";"+ str(row) + ";"+ str(col)
        self.buffer_send += string
        self.send()
        self.set_buffer_send("")
        return
    
    
    def read(self):
        if not self.online:
            return
        
        
        tab = self.buffer_receive.split(";")
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

    def send(self):
        if not self.online:
            return
        
        self.libNetwork.sendC(self.buffer_send.encode())

    """def receive(self,buffer):
        if len(buffer) > 0:
            self.buffer_receive = buffer.decode()
            self.read()"""

    def receive_thread(self):
        if not self.online:
            return
        while not self.thread_stop_event.is_set():
            self.buffer_receive=""
            self.sock = self.libNetwork.createSocket()
            buffer = self.libNetwork.recvC(self.sock)
            if buffer is not None and len(buffer)>0:
                self.buffer_receive = buffer.decode()
                Chat.get_instance().display_received_message(self.buffer_receive)
                self.read()
                self.libNetwork.sendC("hello".encode())
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
    



    @staticmethod
    def get_instance():
        if Multiplayer_connection.instance is None:
            Multiplayer_connection.instance = Multiplayer_connection()
        return Multiplayer_connection.instance