import pygame as pg
from pygame.locals import *

import backup_game
from components import button
from events.event_manager import EventManager
from game.utils import draw_text
from sounds.sounds import SoundManager

pg.font.init()
class Menu:
    def __init__(self, screen):
        self.room_menu = False
        self.loading_menu = False
        self.main_menu = True
        self.splash_screen = True
        self.active = True
        self.save_loading = False
        self.type_text = ""

        self.screen = screen
        self. graphics = self.load_images()
        self.sound_manager = SoundManager()

        # (Width, Height)
        button_size = (322, 32)
        button_start = (self.screen.get_size()[0]/2) - (button_size[0]/2)

        self.button__start_new_career = button.Button((button_start, 350),button_size,
                                                      image=pg.image.load('assets/menu_sprites/start.png').convert(),
                                                      image_hover=pg.image.load('assets/menu_sprites/start_hover.png').convert())
        self.button__start_new_career.on_click(self.set_inactive)

        self.button__load_saved_game = button.Button((button_start, 400), button_size,
                                                      image=pg.image.load('assets/menu_sprites/load saved game.png').convert(),
                                                      image_hover=pg.image.load('assets/menu_sprites/load_saved_game_mouse_on.png').convert())
        self.button__load_saved_game.on_click(self.set_loading_menu)

        self.button__connexion = button.Button((button_start, 450), button_size,
                                                      image=pg.image.load('assets/menu_sprites/multiplayer.png').convert(),
                                                      image_hover=pg.image.load('assets/menu_sprites/multiplayer_sombre.png').convert())
        #self.button__options.set_disabled(True)
        self.button__connexion.on_click(self.set_room_menu)


        self.button__exit = button.Button((button_start, 500), button_size,
                                                      image=pg.image.load('assets/menu_sprites/exit.png').convert(),
                                                      image_hover=pg.image.load('assets/menu_sprites/exit_hover.png').convert())
        self.button__exit.on_click(exit)
        
        self.button__join = button.Button(((self.screen.get_size()[0] / 2) - 150, self.screen.get_size()[1]/3), (70, 20),
                                                      image=pg.image.load('assets/menu_sprites/join.png').convert())
        self.button__join.on_click(exit)
        
        self.button__create_room= button.Button(((self.screen.get_size()[0]/2)+30, self.screen.get_size()[1]/3), (70,20),
                                                      image=pg.image.load('assets/menu_sprites/create_room.png').convert())
        self.button__create_room.on_click(exit)

        self.save1 = button.Button((button_start, 300), button_size, text="Save1")
        self.save1.on_click(self.set_inactive)

        self.save2 = button.Button((button_start, 350), button_size, text="Save2")
        #self.save2.on_click(self.load_save)

        self.save3 = button.Button((button_start, 400), button_size, text="Save3")
        #self.save3.set_disabled(True)

        self.save4 = button.Button((button_start, 450), button_size, text="Save4")
        #self.save4.on_click(exit)

        self.come_back_to_main_menu = button.Button((button_start, 500), (50,45), text="<")
        self.come_back_to_main_menu.on_click(self.set_main_menu)


        if self.is_load_menu() and not self.main_menu:
            EventManager.set_any_input(self.event_load_menu)
        else:
            EventManager.set_any_input(self.skip_splashscreen)
        self.screen.blit(self.graphics["splash"], (0, 0))
        pg.display.flip()

        pg.mixer.music.load('sounds/wavs/ROME4.WAV')
        pg.mixer.music.set_volume(0.6)
        pg.mixer.music.play(0, 0, 2000)


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
        if self.is_load_menu() and not self.main_menu:
            draw_text("Load a City", self.screen,(logo_start+70, 200), color=(255, 255, 200), size=32)
            #print(backup_game.list_fichiers)
            self.save1.display(self.screen)
            self.save2.display(self.screen)
            self.save3.display(self.screen)
            self.save4.display(self.screen)
            self.come_back_to_main_menu.display(self.screen)
            self.event_load_menu()
        if self.room_menu and not self.main_menu and not self.is_load_menu():
            EventManager.clear_components()
            EventManager.clear_hooked_functions()
            EventManager.clear_any_input()
            EventManager.clear_mouse_listeners()
            self.add_input_listener()
            self.come_back_to_main_menu.display(self.screen)
            EventManager.register_component(self.come_back_to_main_menu)
            self.room_menu_set()
        




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
        self.active = False
        pg.mixer.music.stop()

    def skip_splashscreen(self):
        EventManager.clear_any_input()
        self.splash_screen = False
        EventManager.register_component(self.button__start_new_career)
        EventManager.register_component(self.button__load_saved_game)
        EventManager.register_component(self.button__connexion)
        EventManager.register_component(self.button__exit)

    def event_load_menu(self):
        EventManager.clear_any_input()
        self.main_menu = False
        EventManager.remove_component(self.button__start_new_career)
        EventManager.remove_component(self.button__load_saved_game)
        EventManager.remove_component(self.button__connexion)
        EventManager.remove_component(self.button__exit)
        EventManager.register_component(self.save1)
        EventManager.register_component(self.save2)
        EventManager.register_component(self.save3)
        EventManager.register_component(self.save4)
        EventManager.register_component(self.come_back_to_main_menu)
    
    def room_menu_set(self):#fonctionne uniquement quand on est dans la boucle des events
        #en gros on récup que les touches pendant que le programme tourne sur cette fonction
        font = pg.font.Font(None, 24)
        new_text= "Please enter RoomID"
        font2 = pg.font.Font(None, 40)
        text = font2.render(new_text, True, (245,245,220))
        text_2 = font.render(self.type_text, True, (0, 0, 0))
        x = self.screen.get_size()
        zone_de_texte= pg.image.load("assets/menu_sprites/zone_txt.png")
        zone_de_texte= pg.transform.scale(zone_de_texte, (300,50))
        self.button__join.display(self.screen)
        self.button__create_room.display(self.screen)
        self.screen.blit(zone_de_texte, ((x[0] / 2) - 150, (x[1] / 4) + 30))
        self.screen.blit(text,((x[0] / 2)- 165 , (x[1] / 4) ))
        self.screen.blit(text_2, ((x[0] / 2 )-100 , (x[1] / 4) +40))




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
        self.loading_menu = True
        self.main_menu = False
        self.room_menu = False

    def set_main_menu(self):
        self.main_menu = True
        self.loading_menu = False
        self.room_menu = False
        self.skip_splashscreen()

    def set_room_menu(self):
        self.room_menu = True
        self.main_menu = False
        self.room_menu_set()

        

    def add_text(self, key): 
        if key[0] == "backspace":
            self.type_text = self.type_text[:-1]
        else:
            self.type_text+=key[0]
        return
    
    def add_input_listener(self):
        EventManager.register_key_listener(pg.K_a, self.add_text, params = ['a'])
        EventManager.register_key_listener(pg.K_b, self.add_text, params = ['b'])
        EventManager.register_key_listener(pg.K_c, self.add_text, params = ['c'])
        EventManager.register_key_listener(pg.K_d, self.add_text, params = ['d'])
        EventManager.register_key_listener(pg.K_e, self.add_text, params = ['e'])
        EventManager.register_key_listener(pg.K_f, self.add_text, params = ['f'])
        EventManager.register_key_listener(pg.K_g, self.add_text, params = ['g'])
        EventManager.register_key_listener(pg.K_h, self.add_text, params = ['h'])
        EventManager.register_key_listener(pg.K_i, self.add_text, params = ['i'])
        EventManager.register_key_listener(pg.K_j, self.add_text, params = ['j'])
        EventManager.register_key_listener(pg.K_k, self.add_text, params = ['k'])
        EventManager.register_key_listener(pg.K_l, self.add_text, params = ['l'])
        EventManager.register_key_listener(pg.K_m, self.add_text, params = ['m'])
        EventManager.register_key_listener(pg.K_n, self.add_text, params = ['n'])
        EventManager.register_key_listener(pg.K_o, self.add_text, params = ['o'])
        EventManager.register_key_listener(pg.K_p, self.add_text, params = ['p'])
        EventManager.register_key_listener(pg.K_q, self.add_text, params = ['q'])
        EventManager.register_key_listener(pg.K_r, self.add_text, params = ['r'])
        EventManager.register_key_listener(pg.K_s, self.add_text, params = ['s'])
        EventManager.register_key_listener(pg.K_t, self.add_text, params = ['t'])
        EventManager.register_key_listener(pg.K_u, self.add_text, params = ['u'])
        EventManager.register_key_listener(pg.K_v, self.add_text, params = ['v'])
        EventManager.register_key_listener(pg.K_w, self.add_text, params = ['w'])
        EventManager.register_key_listener(pg.K_x, self.add_text, params = ['x'])
        EventManager.register_key_listener(pg.K_y, self.add_text, params = ['y'])
        EventManager.register_key_listener(pg.K_z, self.add_text, params = ['z'])
        EventManager.register_key_listener(pg.K_1, self.add_text, params = ['1'])
        EventManager.register_key_listener(pg.K_2, self.add_text, params = ['2'])
        EventManager.register_key_listener(pg.K_3, self.add_text, params = ['3'])
        EventManager.register_key_listener(pg.K_4, self.add_text, params = ['4'])
        EventManager.register_key_listener(pg.K_5, self.add_text, params = ['5'])
        EventManager.register_key_listener(pg.K_6, self.add_text, params = ['6'])
        EventManager.register_key_listener(pg.K_7, self.add_text, params = ['7'])
        EventManager.register_key_listener(pg.K_8, self.add_text, params = ['8'])
        EventManager.register_key_listener(pg.K_9, self.add_text, params = ['9'])
        EventManager.register_key_listener(pg.K_0, self.add_text, params = ['0'])
        EventManager.register_key_listener(pg.K_SPACE, self.add_text, params = [' '])
        EventManager.register_key_listener(pg.K_BACKSPACE, self.add_text, params = ['backspace'])

        return
    

    def remove_input_listener(self):
        EventManager.remove_key_listener(pg.K_a)
        EventManager.remove_key_listener(pg.K_b)
        EventManager.remove_key_listener(pg.K_c)
        EventManager.remove_key_listener(pg.K_e)
        EventManager.remove_key_listener(pg.K_f)
        EventManager.remove_key_listener(pg.K_g)
        EventManager.remove_key_listener(pg.K_h)
        EventManager.remove_key_listener(pg.K_i)
        EventManager.remove_key_listener(pg.K_j)
        EventManager.remove_key_listener(pg.K_k)
        EventManager.remove_key_listener(pg.K_l)
        EventManager.remove_key_listener(pg.K_m)
        EventManager.remove_key_listener(pg.K_n)
        EventManager.remove_key_listener(pg.K_o)
        EventManager.remove_key_listener(pg.K_p)
        EventManager.remove_key_listener(pg.K_q)
        EventManager.remove_key_listener(pg.K_r)
        EventManager.remove_key_listener(pg.K_s)
        EventManager.remove_key_listener(pg.K_t)
        EventManager.remove_key_listener(pg.K_u)
        EventManager.remove_key_listener(pg.K_v)
        EventManager.remove_key_listener(pg.K_w)
        EventManager.remove_key_listener(pg.K_x)
        EventManager.remove_key_listener(pg.K_y)
        EventManager.remove_key_listener(pg.K_z)
        EventManager.remove_key_listener(pg.K_1)
        EventManager.remove_key_listener(pg.K_2)
        EventManager.remove_key_listener(pg.K_3)
        EventManager.remove_key_listener(pg.K_4)
        EventManager.remove_key_listener(pg.K_5)
        EventManager.remove_key_listener(pg.K_6)
        EventManager.remove_key_listener(pg.K_7)
        EventManager.remove_key_listener(pg.K_8)
        EventManager.remove_key_listener(pg.K_9)
        EventManager.remove_key_listener(pg.K_0)
        EventManager.register_key_listener(pg.K_SPACE)
        EventManager.register_key_listener(pg.K_BACKSPACE)
        return