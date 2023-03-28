import os
from class_types.buildind_types import BuildingTypes
from class_types.road_types import RoadTypes


class Multiplayer_connection:

    def __init__(self):
        self.buffer_receive = ""
        self.buffer_send = ""
        self.builder = None

        pipe_name = "pythonToC"

        if os.path.exists(pipe_name):
            os.remove(pipe_name)

        os.mkfifo(pipe_name)

    def set_builder(self, builder):
        self.builder = builder

    
    def set_buffer_receive(self, buffer):
        self.buffer_receive = buffer
        return


    def set_buffer_send(self, buffer):
        self.buffer_send = buffer
        return

    
    def write(self, row, col, buildingType="destroy"):
        string = str(buildingType) + ";"+ str(row) + ";"+ str(col)
        print(string)
        self.buffer_send += string
        self.send()
        # self.buffer_receive = self.buffer_send
        # self.read()
        # self.set_buffer_receive("")
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
            type_value = None

        #tab = [type_value, "(28,22)", "(28,20)"]
        self.builder.build_from_start_to_end(type_value, Multiplayer_connection.string_to_tuple(tab[1]), Multiplayer_connection.string_to_tuple(tab[2]))


    
    def send(self):
        return
    
    def receive(self):
        return
    
    
    
    
    def string_to_tuple(string):
        string = string.replace("(", "")
        string = string.replace(")", "")
        string = string.replace(" ", "")

        tab = string.split(",")

        return (int(tab[0]), int(tab[1]))
        
        


        


