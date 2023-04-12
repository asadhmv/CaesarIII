import os
import subprocess
import ctypes
import threading
from class_types.buildind_types import BuildingTypes
from class_types.road_types import RoadTypes
from Online.player import Player

list=[]
class Multiplayer_connection:

    def __init__(self, room = None):
        self.room = room
        self.player = Player()
        self.available_rooms = []
        self.buffer_receive = ""
        self.buffer_send = ""
        self.builder = None
        self.buffer_receive = None
        self.newPlayer = None
        """os.chdir('Online')
        subprocess.run(["gcc",  "-c", "-fPIC", "recv.c"])
        subprocess.run(["gcc",  "-c", "-fPIC", "send.c"])
        subprocess.run(["gcc", "-shared", "-fPIC", "-o", "libNetwork.so", "recv.o", "send.o"])
        os.chdir('..')"""
        self.libNetwork = ctypes.cdll.LoadLibrary('Online/libNetwork.so')
        self.libNetwork.recvC.restype = ctypes.c_char_p
        self.libNetwork.sendC.argtypes = [ctypes.c_char_p, ctypes.c_char_p]
        self.libNetwork.sendC_broadcast.argtypes = [ctypes.c_char_p]
        self.sock = None
        self.chat = None
        self.thread_stop_event = threading.Event()
        self.thread = threading.Thread(target=self.receive_thread)
        self.thread.start()

    def get_room(self):
        return self.room

    def set_builder(self, builder):
        self.builder = builder

    def get_player(self):
        return self.player

    def set_buffer_send(self, buffer):
        self.buffer_send = buffer
        return
    def set_buffer_receive(self, buffer):
        self.buffer_receive = buffer
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
        for player in self.get_room().get_players():
            if player.get_ip() != self.player.get_ip():
                self.libNetwork.sendC(self.buffer_send.encode(), player.get_ip().encode())

    def send_specific_buffer(self, message :str):
        for player in self.get_room().get_players():
            if player.get_ip() != self.player.get_ip():
                self.libNetwork.sendC(message.encode(), player.get_ip().encode())

    def send_broadcast(self, message):
        self.libNetwork.sendC_broadcast(message.encode())
        

    
    # def send_message(self, message: str):

    #     message_str = f"{self.player.get_username()}: {message}"
    #     self.libNetwork.sendC_broadcast(message_str.encode())
    
    # def receive_message(self, message: str):
    #     self.chat.display_received_message(message, self.player.get_username())

    def receive_thread(self):
        while not self.thread_stop_event.is_set():
            self.buffer_receive=""
            self.sock = self.libNetwork.createSocket()
            buffer = self.libNetwork.recvC(self.sock)

            if buffer is not None and len(buffer)>0:
                buffer = buffer.decode()
                if "$#[|Who is Room Creator?|]#$" in buffer:
                    #print(self.amItheCreatorOfRoom())
                    if self.room is not None and self.room.amIcreator():
                        creator_buffer = self.room.get_info_in_buffer()
                        joiningPlayerIp = buffer[28 : ]
                        #print(joiningPlayerIp.encode())
                        self.libNetwork.sendC(creator_buffer.encode(), joiningPlayerIp.encode())
                        #print("Envoyé")
                elif "RoomId" in buffer and "NbOfPlayers" in buffer and "Players" in buffer:
                    self.available_rooms.append(buffer)
                    # print("Buffer : ",buffer)
                    # print("List :", self.available_rooms)
                    # print("Received a room")
                elif "Connecting:" in buffer:
                    connecting_player = buffer[11 : ]
                    cp_info = connecting_player.split("=")
                    connecting_player_username = cp_info[0]
                    connecting_player_ip = cp_info[1]
                    p = Player()
                    p.set_ip(connecting_player_ip)
                    p.set_username(connecting_player_username)
                    self.room.addPlayer(p)
                    self.newPlayer = p.get_username()
                elif "$chat:" in buffer:
                    if self.chat is not None :
                        self.chat.add_message_received(buffer)
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
        existingRoomsRequest = "$#[|Who is Room Creator?|]#$" + self.player.get_ip()
        self.libNetwork.sendC_broadcast(existingRoomsRequest.encode())

    def amItheCreatorOfRoom(self) -> bool:
        if self.room is not None:
            creator = self.room.get_creator()
            libPlayer = ctypes.cdll.LoadLibrary('Online/libPlayer.so')
            libPlayer.get_myIP.restype = ctypes.c_char_p
            ip= libPlayer.get_myIP().decode()
            if creator[ip]:
                return True
            return False
        return False
    
    def get_available_rooms(self):
        print("dans le get : ", self.available_rooms)
        return self.available_rooms
    
    def get_newPlayer(self):
        return self.newPlayer
    
    def reset_newPlayer(self):
        self.newPlayer = None
    

    def set_chat(self, chat):
        self.chat = chat