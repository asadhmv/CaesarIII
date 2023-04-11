import pygame as pg

from pygame import Surface, Rect, Color
from components.component import Component
from game import utils
from sounds.sounds import SoundManager
from components.text import Text
from events.event_manager import EventManager

TEXT_COLOR = Color(27, 27, 27)

BASE_COLOR = Color(154, 146, 121)
HOVER_COLOR = Color(139, 131, 106)
SELECTED_COLOR = Color(139, 131, 106)
DISABLED_COLOR = Color(120, 120, 90)

class Input_text():
    def __init__(self, pos, legende:Text, zonetext, defaultText:Text):
        self.pos = pos
        self.legende = legende
        self.zonetext = zonetext
        self.inputText = defaultText


    def display(self, screen: Surface):
        screen.blit(self.zonetext, self.pos)
        self.legende.display(screen)
        self.inputText.display(screen)
        return
    
    
    def add_text(self, key): 
        if key[0] == "backspace":
            self.inputText.setString(self.inputText.getString()[:-1])
        elif len(self.inputText.getString()) == 15:
            return
        else:
            self.inputText.setString(self.inputText.getString()+key[0])
        return
    
    def getString(self):
        return self.inputText.getString()

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
    
    
    @staticmethod
    def remove_input_listener():
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
        EventManager.remove_key_listener(pg.K_SPACE)
        EventManager.remove_key_listener(pg.K_BACKSPACE)
        return

    def clear_inputText(self):
        self.inputText.setString("")