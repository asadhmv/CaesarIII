import pygame as pg

from pygame import Surface, Rect, Color
from components.component import Component
from game import utils
from sounds.sounds import SoundManager


class Text:

    def __init__(self, string, size, pos, color, font=None):
        self.string = string
        self.size=size
        self.pos = pos
        self.color = color
        if font == None:
            self.font = pg.font.Font(None, self.size)
        else:
            self.font = font
        
        self.text = self.font.render(self.string, True, self.color)

    def display(self, screen, pos=False):            
        if not pos:
            screen.blit(self.text, self.pos)
        else:
            screen.blit(self.text, pos)

    def setString(self, string):
        self.string = string
        self.text = self.font.render(string, True, self.color)

    def getString(self):
        return self.string