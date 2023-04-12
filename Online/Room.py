from Online.player import Player

class Room():
    
    def __init__(self, nbJoueur : int, id : str, play_mode=None, mdp : str = False, owner : bool = False):

        self.players=[]
        self.nbJoueur = nbJoueur
        self.mdp = mdp
        self.id = id
        self.owner = owner
        self.creator = {}
        self.play_mode = play_mode

    def addMySelf(self, player : Player):
        self.players.append(player)
        self.creator = {player.get_ip() : player.get_username()}

    def addPlayer(self, player : Player):
        if(len(self.players)==self.nbJoueur):
            return "La room est complète"
        else:
            self.players.append(player)
            return True
    
    def removePlayer(self, player):
        self.players.remove(player)
    

    def join(self, player, id, mdp = False):
        if mdp == self.mdp and id == self.id:
            return self.addPlayer(player)
        else:
            return "ID ou mot de passe incorrecte"

    def get_creator(self):
        return self.creator
    
    def amIcreator(self):
        return self.owner

    def get_info(self):
        return {'room_id' : self.id,
                'nb_players': self.nbJoueur,
                'players' : self.players}
    
    def get_info_in_buffer(self):
        room = self.get_info()
        buffer = 'RoomId=' + room['room_id'] + ';'
        buffer += 'NbOfPlayers=' + str(room['nb_players']) + ';' 
        buffer += 'Players='

        for i in range(len(self.players)):
            player = self.players[i]
            buffer += player.get_username() + ":" + player.get_ip()
            if i == len(self.players) - 1:
                buffer += ";"
            else:
                buffer += ","

        return buffer

    def get_players(self) -> list:
        return self.players


    # def create(self,room_name, player):
    #     if room_name in self.rooms:
    #         return False
    #     else:
    #         self.rooms[room_name]= [player]
    #         print("created room")
    #         return True

    # def join(self,room_name, player):
    #     if room_name in self.rooms:
    #         self.rooms[room_name].append(player)
    #         print("Exist")
    #         print(self.rooms)
    #         return True
    #     return False