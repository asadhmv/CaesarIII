import os
import subprocess
import ctypes
#import thread
import threading
from class_types.buildind_types import BuildingTypes
from class_types.road_types import RoadTypes


class Multiplayer_connection:

    def __init__(self):
        self.buffer_receive = ""
        self.buffer_send = ""
        self.builder = None
        self.buffer_receive = None
        self.thread = threading.Thread(target=self.receive_thread)
        self.libNetwork = ctypes.cdll.LoadLibrary('Online/libNetwork.so')
        self.libNetwork.recvC.restype = ctypes.c_char_p
        self.libNetwork.sendC.argtypes = [ctypes.c_char_p]
        self.thread.start()


    def set_builder(self, builder):
        self.builder = builder

    



    def set_buffer_send(self, buffer):
        self.buffer_send = buffer
        return

    
    def write(self, row, col, buildingType="destroy"):
        string = str(buildingType) + ";"+ str(row) + ";"+ str(col)
        self.buffer_send += string
        self.send()
        self.set_buffer_send("")
        return
    
    def read(self):
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
        self.libNetwork.sendC(self.buffer_send.encode())

    def receive(self,buffer):
        if len(buffer) > 0:
            self.buffer_receive = buffer.decode()
            self.read()

    def receive_thread(self):
        while True:
            self.buffer_receive=""
            self.buffer_receive = self.libNetwork.recvC()
            thread = threading.Thread(target=self.receive,args=(self.buffer_receive,))
            thread.start()



    def string_to_tuple(string):
        string = string.replace("(", "")
        string = string.replace(")", "")
        string = string.replace(" ", "")

        tab = string.split(",")

        return (int(tab[0]), int(tab[1]))

        
