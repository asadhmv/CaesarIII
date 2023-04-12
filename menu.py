import pygame as pg
from compet_mode import Comp_mode
from pygame.locals import *
import time

import backup_game
from components import button
from components.input_text import Input_text
from components.text import Text
from events.event_manager import EventManager
from game.utils import draw_text
from sounds.sounds import SoundManager
from Online.Room import Room
from Online.player import Player
from Online.multiplayer_connection import Multiplayer_connection

pg.font.init()
class Menu:
    def __init__(self, screen):
        self.multiplayer = Multiplayer_connection()
        self.room_menu = False
        self.loading_menu = False
        self.main_menu = True
        self.username_menu = False
        self.roomSettings_menu = False
        self.roomPassword_menu = False
        self.gamemode = False
        self.roomId_menu = False
        self.join_create_menu = False
        self.listRoom_menu = False
        self.splash_screen = True
        self.active = True
        self.save_loading = False
        self.nbPlayer = 1
        self.online = True
        self.join = False
        self.listRoom = []


        self.screen = screen
        self. graphics = self.load_images()
        self.sound_manager = SoundManager()
        

        # (Width, Height)
        button_size = (322, 32)
        button_start = (self.screen.get_size()[0]/2) - (button_size[0]/2)


        #------------------MAIN MENU
        self.button__start_new_career = button.Button((button_start, 350),button_size,
                                                      image=pg.image.load('assets/menu_sprites/start.png').convert(),
                                                      image_hover=pg.image.load('assets/menu_sprites/start_hover.png').convert())
        self.button__start_new_career.on_click(self.set_inactive_offline)

        self.button__load_saved_game = button.Button((button_start, 400), button_size,
                                                      image=pg.image.load('assets/menu_sprites/load saved game.png').convert(),
                                                      image_hover=pg.image.load('assets/menu_sprites/load_saved_game_mouse_on.png').convert())
        self.button__load_saved_game.on_click(self.set_loading_menu)

        self.button__connexion = button.Button((button_start, 450), button_size,
                                                      image=pg.image.load('assets/menu_sprites/multiplayer.png').convert(),
                                                      image_hover=pg.image.load('assets/menu_sprites/multiplayer_sombre.png').convert())
        #self.button__options.set_disabled(True)
        self.button__connexion.on_click(self.set_join_create_menu)


        self.button__exit = button.Button((button_start, 500), button_size,
                                                      image=pg.image.load('assets/menu_sprites/exit.png').convert(),
                                                      image_hover=pg.image.load('assets/menu_sprites/exit_hover.png').convert())
        self.button__exit.on_click(self.exit)
        

        
        
        




        #------------------SAVES MENU
        self.save1 = button.Button((button_start, 300), button_size, text="Save1")
        self.save1.on_click(self.set_inactive_offline)

        self.save2 = button.Button((button_start, 350), button_size, text="Save2")
        #self.save2.on_click(self.load_save)

        self.save3 = button.Button((button_start, 400), button_size, text="Save3")
        #self.save3.set_disabled(True)

        self.save4 = button.Button((button_start, 450), button_size, text="Save4")
        #self.save4.on_click(exit)

        self.come_back_to_main_menu = button.Button((button_start, 500), (50,45), text="<", center_text=True)
        self.come_back_to_main_menu.on_click(self.set_main_menu)

    


        #------------------USERNAME MENU
        self.size_screen = self.screen.get_size()
        legende_username = Text("Please enter Username", 40, (self.size_screen[0]/2.4, self.size_screen[1]/4), (245,245,220))
        typeText_username = Text("", 24, (self.size_screen[0]/2-135, self.size_screen[1]/4+50), (0,0,0))
        zone_de_texte = pg.image.load("assets/menu_sprites/zone_txt.png")
        zone_de_texte = pg.transform.scale(zone_de_texte, (300,50))
        self.input_username = Input_text((self.size_screen[0]/2.4, self.size_screen[1]/4+30), legende_username, zone_de_texte, typeText_username)
        #self.valide_username = button.Button((0,0), (self.size_screen[0]/20,self.size_screen[1]/25), text="Valider", text_size=20, center_text=True)
        self.valide_username = button.Button((self.size_screen[0]/2,self.size_screen[1]/3), (self.size_screen[0]/15,self.size_screen[1]/20), text="Valider", text_size=20, center_text_mod2=True)
        self.valide_username.on_click(self.set_inactive, self.create_room)
        self.type=typeText_username

        #------------------ROOM ID MENU
        legende = Text("Please enter RoomID", 40, (self.size_screen[0]/2.4, self.size_screen[1]/4), (245,245,220))
        typeText = Text("", 24, (self.size_screen[0]/2-135, self.size_screen[1]/4+50), (0,0,0))
        zone_de_texte= pg.image.load("assets/menu_sprites/zone_txt.png")
        zone_de_texte= pg.transform.scale(zone_de_texte, (300,50))
        self.input_room = Input_text((self.size_screen[0]/2.4, self.size_screen[1]/4+30), legende, zone_de_texte, typeText)
        self.valide_idRoom = button.Button((self.size_screen[0]/2,self.size_screen[1]/3), (self.size_screen[0]/15,self.size_screen[1]/20), text="Valider", text_size=20, center_text_mod2=True)
        self.valide_idRoom.on_click(self.set_username_menu)

        #------------------JOIN/CREATE MENU
        self.button__join = button.Button(((self.screen.get_size()[0] / 2.4), self.screen.get_size()[1]/3), (70, 20),
                                                      image=pg.image.load('assets/menu_sprites/join.png').convert())
        self.button__join.on_click(self.set_listRoom_menu)
        
        self.button__create_room= button.Button(((self.screen.get_size()[0]/2), self.screen.get_size()[1]/3), (70,20),
                                                      image=pg.image.load('assets/menu_sprites/create_room.png').convert())
        self.button__create_room.on_click(self.set_roomSettings_menu)
        self.choose_modemenu = button.Button((self.size_screen[0] / 2.35, self.size_screen[1] / 2.6), (200, 30), text="Choose game mode", text_size=20, center_text=True)
        self.choose_modemenu.on_click(self.set_gamemode)

        #------------------ROOM SETTINGS MENU
        self.nbPlayerText = Text("Nombre de joueur maximum : "+str(self.nbPlayer), 30, (self.size_screen[0]/2.4, self.size_screen[1]/2.9), (0,0,0))
        self.plus = button.Button((self.size_screen[0]/1.95, self.size_screen[1]/2.6), (self.size_screen[0]/30,self.size_screen[1]/25), text="+", text_size=40, center_text=True)
        self.moins = button.Button((self.size_screen[0]/2.35, self.size_screen[1]/2.6), (self.size_screen[0]/30,self.size_screen[1]/25), text="-", text_size=40, center_text=True)
        self.plus.on_click(self.incrementNbPlayer)
        self.moins.on_click(self.decrementNbPlayer)
        
        self.roomPublicText = Text("Room is Public", 30, (self.size_screen[0]/2.2, self.size_screen[1]/4), (0,0,0))
        self.public_button = button.Button((self.size_screen[0]/2, self.size_screen[1]/3.6), (self.size_screen[0]/15,self.size_screen[1]/20), text="Public", text_size=20, center_text_mod2=True)
        self.private_button = button.Button((self.size_screen[0]/2.4, self.size_screen[1]/3.6), (self.size_screen[0]/15,self.size_screen[1]/20), text="Private", text_size=20, center_text_mod2=True)
        self.public_button.on_click(self.set_roomPublic)
        self.private_button.on_click(self.set_roomPrive)

        self.size_screen = self.screen.get_size()
        legende_password = Text("Please enter password", 40, (self.size_screen[0]/2.4, self.size_screen[1]/6), (245,245,220))
        typeText_password = Text("", 24, (self.size_screen[0]/2-135, self.size_screen[1]/6+50), (0,0,0))


        size_screen = self.screen.get_size()
        legende_password = Text("Please enter password", 40, (self.size_screen[0]/2.4, self.size_screen[1]/6), (245,245,220))
        typeText_password = Text("", 24, (self.size_screen[0]/2-135, self.size_screen[1]/6+50), (0,0,0))
        zone_de_texte = pg.image.load("assets/menu_sprites/zone_txt.png")
        zone_de_texte = pg.transform.scale(zone_de_texte, (300,50))
        self.input_password = Input_text((self.size_screen[0]/2.4, self.size_screen[1]/6+30), legende_password, zone_de_texte, typeText_password)
        self.valide_settings = button.Button((self.size_screen[0]/2,self.size_screen[1]/2.17), (self.size_screen[0]/15,self.size_screen[1]/20), text="Valider", text_size=20, center_text_mod2=True)
        self.valide_settings.on_click(self.set_roomId_menu)
        #self.valide_settings.on_click(self.set_inactive, self.create_room)

        #------------------LIST ROOM MENU
        self.listRoomButtons = []
        self.roomChosen = None
        self.refresh_button = button.Button((self.size_screen[0]/2,self.size_screen[1]/2.17), (self.size_screen[0]/15,self.size_screen[1]/20), text="Refresh", text_size=20, center_text_mod2=True)
        self.refresh_button.on_click(self.refresh)

        self.gamemodeChoice1 = button.Button((self.size_screen[0]/2.35-50, self.size_screen[1]/4), (400, 40), text="ATTACK MODE", text_size=20, center_text_mod2=True)
        self.gamemodeChoice2 = button.Button((self.size_screen[0]/2.35-50, (self.size_screen[1]/4)+50), (400, 40), text="COMPETITION MODE", text_size=20, center_text_mod2=True)
        self.gamemodeChoice3 = button.Button((self.size_screen[0] / 2.35-50, (self.size_screen[1] / 4)+100), (400, 40), text="OPEN WORLD MODE", text_size=20, center_text_mod2=True)
        self.gamemodeChoice1.on_click(exit)
        self.gamemodeChoice2.on_click(self.comp)
        self.gamemodeChoice3.on_click(exit)

        if self.is_load_menu() and not self.main_menu:
            EventManager.set_any_input(self.event_load_menu)
        else:
            EventManager.set_any_input(self.skip_splashscreen)
        self.screen.blit(self.graphics["splash"], (0, 0))
        pg.display.flip()

        pg.mixer.music.load('sounds/wavs/ROME4.WAV')
        pg.mixer.music.set_volume(0.6)
        pg.mixer.music.play(0, 0, 2000)

    def exit(self):
        if self.multiplayer is not None:
            self.multiplayer.kill_thread()
        self.set_inactive_offline()

    def create_room(self):
        if not self.join:
            self.room = Room(self.nbPlayer, self.input_room.getString(), owner=True)
            myself = self.get_multiplayer().get_player()
            self.room.addPlayer(myself)
        elif self.join:
            self.join_room(self.choosenRoom)

        self.multiplayer.set_room(self.room)

        print("Players in this Room :")
        for p in self.room.get_players():
            print("Username = " + p.get_username() + ", IP = " +p.get_ip())

    def get_room(self):
        #return self.room
        pass

    def run(self):
        EventManager.handle_events()
        if self.is_splashscreen_skipped():
            self.affichage()


    def affichage(self):
        self.screen.blit(self.graphics["background"], (0, 0))
        #self.sound_manager.play('menu_demarrer')

        rect_size = (500, 400)
        rect_pos = ((self.screen.get_size()[0]/2) - (rect_size[0]/2), 180)
        rect = pg.Rect(rect_pos, rect_size)
        pg.draw.rect(self.screen, (60, 40, 25), rect)

        logo_start = (self.screen.get_size()[0]/2) - (self.graphics["logo"].get_size()[0]/2)

        if self.main_menu:
            self.screen.blit(self.graphics["logo"], (logo_start, 200))
            self.button__start_new_career.display(self.screen)
            self.button__load_saved_game.display(self.screen)
            self.button__connexion.display(self.screen)
            self.button__exit.display(self.screen)
        elif self.is_load_menu() and not self.main_menu:
            draw_text("Load a City", self.screen,(logo_start+70, 200), color=(255, 255, 200), size=32)
            #print(backup_game.list_fichiers)
            self.save1.display(self.screen)
            self.save2.display(self.screen)
            self.save3.display(self.screen)
            self.save4.display(self.screen)
            self.come_back_to_main_menu.display(self.screen)
            self.event_load_menu()
        elif self.room_menu:
            self.room_menu_display()
        elif self.username_menu:
            self.username_menu_display()
        elif self.roomSettings_menu:
            self.roomSettings_menu_display()
        elif self.roomId_menu:
            self.roomId_menu_display()
        elif self.listRoom_menu:
            self.room_list_display()
        elif self.join_create_menu:
            self.join_create_menu_display()
        elif self.gamemode:
            self.gamemode_menu_display()




        pg.display.flip()

    def load_images(self):
        background = pg.image.load('assets/menu_sprites/background_menu.jpg').convert()
        background = pg.transform.scale(background, self.screen.get_size())

        logo = pg.image.load('assets/menu_sprites/caesar3.png').convert_alpha()
        logo = pg.transform.scale(logo, (440, 130))

        splash = pg.image.load('assets/menu_sprites/splash_screen.jpg').convert()
        splash = pg.transform.scale(splash, self.screen.get_size())


        return {
            'background': background,
            'logo': logo,
            'splash': splash
        }

    def is_active(self):
        return self.active

    def set_inactive(self):
        self.multiplayer.get_player().set_username(self.input_username.getString())
        self.active = False
        pg.mixer.music.stop()
    
    def set_inactive_offline(self):
        self.online = False
        self.multiplayer.set_online(False)
        self.active = False
        pg.mixer.music.stop()

    def set_inactive_join(self):
        #self.join = True
        self.multiplayer.getExistingRooms()
        available_rooms = self.multiplayer.get_available_rooms()
        for room in available_rooms:
            print(room)
        #self.set_inactive()


    def comp(self):
        Comp_mode.get_instance().launch_compet_mode()
        self.set_inactive()
    def skip_splashscreen(self):
        EventManager.clear_any_input()
        self.splash_screen = False
        EventManager.register_component(self.button__start_new_career)
        EventManager.register_component(self.button__load_saved_game)
        EventManager.register_component(self.button__connexion)
        EventManager.register_component(self.button__exit)

    def event_load_menu(self):
        EventManager.clear_any_input()
        EventManager.reset()
        self.main_menu = False
        EventManager.register_component(self.save1)
        EventManager.register_component(self.save2)
        EventManager.register_component(self.save3)
        EventManager.register_component(self.save4)
        EventManager.register_component(self.come_back_to_main_menu)
    
    def room_menu_display(self):#fonctionne uniquement quand on est dans la boucle des events
        #en gros on récup que les touches pendant que le programme tourne sur cette fonction
        EventManager.clear_any_input()
        EventManager.reset()
        EventManager.register_component(self.come_back_to_main_menu)
        EventManager.register_component(self.button__create_room)
        EventManager.register_component(self.button__join)
        self.come_back_to_main_menu.display(self.screen)
        self.button__join.display(self.screen)
        self.button__create_room.display(self.screen)

    def room_list_display(self):
        EventManager.reset()
        EventManager.clear_any_input()
        EventManager.register_component(self.come_back_to_main_menu)
        EventManager.register_component(self.refresh_button)
        self.come_back_to_main_menu.display(self.screen)
        self.refresh_button.display(self.screen)

        for button in self.listRoomButtons:
            EventManager.register_component(button)
            button.display(self.screen)
        return


    def roomId_menu_display(self):
        EventManager.clear_any_input()
        EventManager.reset()
        EventManager.register_component(self.come_back_to_main_menu)
        EventManager.register_component(self.valide_idRoom)
        EventManager.register_component(self.choose_modemenu)
        self.input_room.display(self.screen)
        self.input_room.add_input_listener()
        self.come_back_to_main_menu.display(self.screen)
        self.valide_idRoom.display(self.screen)
        return

    def join_create_menu_display(self):
        EventManager.clear_any_input()
        EventManager.reset()
        EventManager.register_component(self.come_back_to_main_menu)
        EventManager.register_component(self.button__create_room)
        EventManager.register_component(self.button__join)
        EventManager.register_component(self.choose_modemenu)
        self.come_back_to_main_menu.display(self.screen)
        self.button__join.display(self.screen)
        self.button__create_room.display(self.screen)
        self.choose_modemenu.display(self.screen)

    def gamemode_menu_display(self):
        EventManager.clear_any_input()
        EventManager.remove_component(self.button__start_new_career)
        EventManager.remove_component(self.button__load_saved_game)
        EventManager.remove_component(self.button__connexion)
        EventManager.remove_component(self.button__exit)
        #EventManager.register_component(self.gamemodeChoice1)
        EventManager.register_component(self.gamemodeChoice2)
        # EventManager.register_component(self.gamemodeChoice3)
        # self.gamemodeChoice1.display(self.screen)
        self.gamemodeChoice2.display(self.screen)
        #self.gamemodeChoice3.display(self.screen)
        self.come_back_to_main_menu.display(self.screen)
        return


    def username_menu_display(self):
        EventManager.clear_any_input()
        EventManager.reset()
        EventManager.register_component(self.valide_username)
        EventManager.register_component(self.come_back_to_main_menu)
        self.input_username.add_input_listener()
        self.input_username.display(self.screen)
        self.valide_username.display(self.screen)
        self.come_back_to_main_menu.display(self.screen)
        return

    def roomSettings_menu_display(self):
        EventManager.clear_any_input()
        EventManager.reset()
        EventManager.register_component(self.plus)
        EventManager.register_component(self.moins)
        EventManager.register_component(self.public_button)
        EventManager.register_component(self.private_button)
        EventManager.register_component(self.come_back_to_main_menu)
        EventManager.register_component(self.valide_settings)
        if self.roomPublicText.getString() == "Room is Private":
            self.input_password.add_input_listener()
            self.input_password.display(self.screen)
        else:
            Input_text.remove_input_listener()
            

        self.public_button.display(self.screen)
        self.private_button.display(self.screen)
        self.roomPublicText.display(self.screen)
        self.plus.display(self.screen)
        self.moins.display(self.screen)
        self.nbPlayerText.display(self.screen)
        self.valide_settings.display(self.screen)
        self.come_back_to_main_menu.display(self.screen)

    def is_splashscreen_skipped(self):
        return not self.splash_screen

    def load_save(self):
        self.save_loading = True
        self.set_inactive()

    def get_save_loading(self):
        return self.save_loading

    def is_load_menu(self):
        return self.loading_menu

    def set_loading_menu(self):
        self.room_menu = False
        self.loading_menu = True
        self.main_menu = False
        self.username_menu = False
        self.roomSettings_menu = False
        self.roomId_menu = False
        self.listRoom_menu = False
        self.join_create_menu = False

    def set_join_create_menu(self):
        self.room_menu = False
        self.loading_menu = False
        self.main_menu = False
        self.username_menu = False
        self.roomSettings_menu = False
        self.roomId_menu = False
        self.listRoom_menu = False
        self.join_create_menu = True

    def set_main_menu(self):
        self.join = False
        self.valide_username.on_click(self.set_inactive, self.create_room)

        self.room_menu = False
        self.loading_menu = False
        self.main_menu = True
        self.username_menu = False
        self.roomSettings_menu = False
        self.roomId_menu = False
        self.listRoom_menu = False
        self.join_create_menu = False
        self.skip_splashscreen()

    def set_room_menu(self):
        self.room_menu = True
        self.loading_menu = False
        self.main_menu = False
        self.username_menu = False
        self.roomSettings_menu = False
        self.roomId_menu = False
        self.listRoom_menu = False
        self.join_create_menu = False
        
    def set_username_menu(self):
        self.room_menu = False
        self.loading_menu = False
        self.main_menu = False
        self.username_menu = True
        self.roomSettings_menu = False
        self.roomId_menu = False
        self.listRoom_menu = False
        self.join_create_menu = False

    
    def set_roomSettings_menu(self):
        self.room_menu = False
        self.loading_menu = False
        self.main_menu = False
        self.username_menu = False
        self.roomSettings_menu = True
        self.roomId_menu = False
        self.listRoom_menu = False
        self.join_create_menu = False

    def set_roomId_menu(self):
        self.room_menu = False
        self.loading_menu = False
        self.main_menu = False
        self.username_menu = False
        self.roomSettings_menu = False
        self.roomId_menu = True
        self.listRoom_menu = False
        self.join_create_menu = False
    
    def set_listRoom_menu(self):
        self.join = True
        self.valide_username.on_click(self.set_inactive, None)

        self.room_menu = False
        self.loading_menu = False
        self.main_menu = False
        self.username_menu = False
        self.roomSettings_menu = False
        self.roomId_menu = False
        self.listRoom_menu = True
        self.join_create_menu = False

        self.refresh()

    def set_choosenRoom(self, room):
        self.choosenRoom = room

    def join_room(self, room : str):
        room_info = room.split(";")
        room_id = room_info[0][ 7 : ]
        room_nbPlayers = room_info[1][12 : ]
        room_players_info = room_info[2][8 : ]
        room_players = room_players_info.split(",")
        self.room = Room(int(room_nbPlayers), room_id, owner=False)

        for player in room_players:
            player_info = player.split(":")
            username = player_info[0]
            ip = player_info[1]
            p = Player()
            p.set_username(username)
            p.set_ip(ip)
            self.room.addPlayer(p)

        myself = self.get_multiplayer().get_player()
        self.room.addPlayer(myself)
        self.multiplayer.set_room(self.room)
        connecting_buffer = "Connecting:" + myself.get_username() + "=" + myself.get_ip()
        self.multiplayer.send_specific_buffer(connecting_buffer)

    def set_gamemode(self):
        self.join_create_menu = False
        self.room_menu = False
        self.loading_menu = False
        self.main_menu = False
        self.username_menu = False
        self.roomSettings_menu = False
        self.roomPassword_menu = False
        self.gamemode = True


    def incrementNbPlayer(self):
        max = 99
        if self.nbPlayer < max:
            self.nbPlayer += 1
            self.nbPlayerText.setString("Nombre de joueur maximum : "+str(self.nbPlayer))
        else:
            return
    
    def decrementNbPlayer(self):
        min = 1
        if self.nbPlayer > min:
            self.nbPlayer -= 1
            self.nbPlayerText.setString("Nombre de joueur maximum : "+str(self.nbPlayer))
        else:
            return


    def set_roomPublic(self):
        self.roomPublicText.setString("Room is Public")
    
    def set_roomPrive(self):
        self.roomPublicText.setString("Room is Private")

    def get_online(self):
        return self.online
    
    def getInformationsRoom(self):
        return {
            "online":self.online,
            "nbPlayer":self.nbPlayer,
            "public":self.roomPublicText,
            "password":self.input_password.getString(),
            "username":self.input_username.getString(),
            "name":self.input_room.getString(),
            "join":self.join,
            "roomChosen":self.roomChosen
            }

    def get_multiplayer(self) -> Multiplayer_connection:
        return self.multiplayer

    def refresh(self):
        self.listRoomButtons.clear()
        self.listRoom.clear()
        self.multiplayer.getExistingRooms()
        time.sleep(1)
        #available_rooms = self.multiplayer.get_available_rooms()

        self.listRoom = self.multiplayer.get_available_rooms()
        print("aaaa :", self.listRoom)

        #self.listRoom = ["salut", "cest moi", "ouf"]
        i = -100
        for room in self.listRoom:
            room_info = room
            room = room.split(";")[0]
            room = room.replace("RoomId=", "")
            tmp_button = button.Button((self.size_screen[0]/2, self.size_screen[1]/3.6+i), (self.size_screen[0]/15,self.size_screen[1]/20), text=room, text_size=20, center_text_mod2=True)
            tmp_button.on_click(self.set_username_menu, lambda: self.set_choosenRoom(room_info))
            self.listRoomButtons.append(tmp_button)
            i+=75