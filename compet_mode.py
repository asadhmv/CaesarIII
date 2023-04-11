from game.game_controller import GameController
import time
import threading
import os
import ctypes
import pygame
from menu import Menu
class Comp_mode:
    instance=None
    def __init__(self):
        self.thread = threading.Thread(target=self.chrono)
        self.thread.start()
        self.thread_stop_event = threading.Event()
        self.libNetwork = ctypes.cdll.LoadLibrary('Online/libNetwork.so')
        self.libNetwork.sendC.argtypes = [ctypes.c_char_p]
        self.score=0
        self.var=""
        self.actived=False


    def chrono(self):
        if self.actived:
            time.sleep(120)
            print("calculate .....")
            self.score=GameController.get_instance().actual_citizen + GameController.get_instance().actual_foods + int(GameController.get_instance().global_desirability)
            self.libNetwork.sendC(str(self.score).encode())



    def kill_chrono(self):
        self.thread_stop_event.set()
        os._exit(0)


    def compare_with_mine(self,value):
        self.score = GameController.get_instance().actual_citizen + GameController.get_instance().actual_foods +int(GameController.get_instance().global_desirability)
        return self.score > value

    def play_score(self,var):
        self.var=var
        print("YOOOO!")
        print("*******"+var+"*******")





    @staticmethod
    def get_instance():
        if Comp_mode.instance is None:
            Comp_mode.instance = Comp_mode()
        return Comp_mode.instance


