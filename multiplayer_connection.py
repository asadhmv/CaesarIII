import os
import subprocess
import ctypes
#import thread
from class_types.buildind_types import BuildingTypes
from class_types.road_types import RoadTypes


class Multiplayer_connection:

    def __init__(self, online=False):
        self.buffer_receive = ""
        self.buffer_send = ""
        self.builder = None
        self.online = online
        self.libNetwork = ctypes.cdll.LoadLibrary('Online/libNetwork.so')
        self.libNetwork.recvC.restype = ctypes.c_char_p
        self.libNetwork.sendC.argtypes = [ctypes.c_char_p]


    def set_builder(self, builder):
        self.builder = builder

    
    def set_buffer_receive(self, buffer):
        self.buffer_receive = buffer
        return


    def set_buffer_send(self, buffer):
        self.buffer_send = buffer
        return

    
    def write(self, row, col, buildingType="destroy"):
        if not self.online:
            return
        
        string = str(buildingType) + ";"+ str(row) + ";"+ str(col)
        self.buffer_send += string
        print(self.buffer_send)
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
            type_value = None

        self.builder.build_from_start_to_end(type_value, Multiplayer_connection.string_to_tuple(tab[1]), Multiplayer_connection.string_to_tuple(tab[2]))


    
    def send(self):
        if not self.online:
            return
        
        self.libNetwork.sendC(self.buffer_send.encode())

    def receive(self):
        if not self.online:
            return
        #os.system("gcc ") 
        self.buffer_receive = self.libNetwork.recvC().decode()
        self.libNetwork.recvC.restype = ctypes.c_char_p
        self.read()
        print(self.buffer_receive)

    def string_to_tuple(string):
        string = string.replace("(", "")
        string = string.replace(")", "")
        string = string.replace(" ", "")

        tab = string.split(",")

        return (int(tab[0]), int(tab[1]))




multiplayer = Multiplayer_connection()
multiplayer.send()
        
