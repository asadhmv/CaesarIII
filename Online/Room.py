class Room():
    
    def __init__(self, nbJoueur, player, id, mdp=False):

        self.players=[player]
        self.nbJoueur = nbJoueur
        self.mdp = mdp
        self.id = id
        print("Room crée")

    def addPlayer(self, player):
        if(len(self.players)==self.nbJoueur):
            return "La room est complète"
        else:
            self.append(player)
            return True
    
    def removePlayer(self, player):
        self.players.remove(player)
    

    def join(self, player, id, mdp = False):
        if mdp == self.mdp and id == self.id:
            return self.addPlayer(player)
        else:
            return "ID ou mot de passe incorrecte"


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