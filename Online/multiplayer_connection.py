import os
import subprocess
import ctypes
import threading
from class_types.buildind_types import BuildingTypes
from class_types.road_types import RoadTypes
from compet_mode import Comp_mode
import pygame
class Multiplayer_connection:


    def __init__(self, room,online=False):
        self.room = room
        self.list_receive = []

        self.buffer_send = ""
        self.builder = None
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
        self.getExistingRooms()
        self.libPlayer = ctypes.cdll.LoadLibrary('Online/libPlayer.so')
        self.libPlayer.get_myIP.restype = ctypes.c_char_p
        self.ip = self.libPlayer.get_myIP().decode()
        Comp_mode.get_instance()


    def set_builder(self, builder):
        self.builder = builder


    def set_buffer_send(self, buffer):
        self.buffer_send = buffer


    
    def write(self, row, col, buildingType="destroy"):

        
        string = str(buildingType) + ";"+ str(row) + ";"+ str(col)
        self.buffer_send += string
        self.send()
        self.set_buffer_send("")


    
    def read(self):

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

        self.builder.build_from_start_to_end(type_value, Multiplayer_connection.string_to_tuple(tab[1]), Multiplayer_connection.string_to_tuple(tab[2]),self.list_receive[0])


    

    def send(self):
        self.libNetwork.sendC(self.buffer_send.encode())



    def receive_thread(self):
        while not self.thread_stop_event.is_set():
            self.list_receive=[]
            self.sock = self.libNetwork.createSocket()
            buffer = self.libNetwork.recvC(self.sock)

            if buffer :
                if buffer[0]:
                    self.list_receive.append(buffer[0].decode('utf-8'))
                if buffer[1]:
                    self.list_receive.append(buffer[1].decode('utf-8'))
                #print(self.list_receive)

                if self.list_receive[1] == "$#[|Who is Room Creator?|]#$":
                    if self.amItheCreatorOfRoom():
                        creator_buffer = self.room.get_info_in_buffer()
                        self.libNetwork.sendC(creator_buffer.encode())


                else:
                    if self.list_receive[0]!=self.ip:
                        var=None
                        try:
                            if Comp_mode.get_instance().compare_with_mine(int(self.list_receive[1])):
                                var=" You "
                            else:
                                var= " "+self.list_receive[0]
                            Comp_mode.get_instance().play_score(var)

                        except ValueError:
                            self.buffer_receive = buffer
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
    
    def getExistingRooms(self):
        existingRoomsRequest = "$#[|Who is Room Creator?|]#$"
        self.libNetwork.sendC(existingRoomsRequest.encode())

    def amItheCreatorOfRoom(self):
    #    creator = self.room.get_creator()
    #    libPlayer = ctypes.cdll.LoadLibrary('Online/libPlayer.so')
    #    libPlayer.get_myIP.restype = ctypes.c_char_p
    #    ip= libPlayer.get_myIP().decode()
    #    if creator[ip]:
    #        return True
    #    return False
        pass



