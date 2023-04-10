import os
import subprocess
import ctypes
import threading
from class_types.buildind_types import BuildingTypes
from class_types.road_types import RoadTypes

class Multiplayer_connection:

    def __init__(self, room = None):
        self.room = room
        self.available_rooms = []
        self.buffer_receive = ""
        self.buffer_send = ""
        self.builder = None
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
        self.getExistingRooms()


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


    def receive_thread(self):
        while not self.thread_stop_event.is_set():
            self.buffer_receive=""
            self.sock = self.libNetwork.createSocket()
            buffer = self.libNetwork.recvC(self.sock)

            if buffer is not None and len(buffer)>0:
                buffer = buffer.decode()
                if buffer == "$#[|Who is Room Creator?|]#$":
                    if self.amItheCreatorOfRoom():
                        creator_buffer = self.room.get_info_in_buffer()
                        self.libNetwork.sendC(creator_buffer.encode())
                elif "RoomId" in buffer and "NbOfPlayers" in buffer and "Players" in buffer:
                    self.available_rooms.append(buffer)
                else:
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
    
    def set_room(self, room):
        self.room = room
    
    def getExistingRooms(self):
        existingRoomsRequest = "$#[|Who is Room Creator?|]#$"
        self.libNetwork.sendC(existingRoomsRequest.encode())

    def amItheCreatorOfRoom(self):
        if self.room is not None:
            creator = self.room.get_creator()
            libPlayer = ctypes.cdll.LoadLibrary('Online/libPlayer.so')
            libPlayer.get_myIP.restype = ctypes.c_char_p
            ip= libPlayer.get_myIP().decode()
            if creator[ip]:
                return True
            return False
    
    def get_available_rooms(self):
        return self.available_rooms



