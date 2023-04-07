
class Rooms():
    def __init__(self):
        
        self.rooms={}

    def create(self,room_name, player):
        if room_name in self.rooms:
            return False
        else:
            self.rooms[room_name]= [player]
            print("created room")
            return True

    def join(self,room_name, player):
        if room_name in self.rooms:
            self.rooms[room_name].append(player)
            print("Exist")
            print(self.rooms)
            return True
        return False
            
