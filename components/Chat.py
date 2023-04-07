import pygame as pg
import tkinter as tk

class Chat:
    def __init__(self,screen):
        self.chat_window = None
        self.entry = None
        self.send_button = None
        self.screen = screen
        self.rect = pg.Surface((300, 600), pg.SRCALPHA, 32)
        self.click_count = 0
        self.send_button = None
        
    def show_chat(self, posx, posy):
        self.rect.fill((255, 255, 255))
        self.screen.blit(self.rect, (posx, posy))
        zone_de_texte= pg.image.load("assets/C3_sprites/C3/zone_msg.png")
        zone_de_texte= pg.transform.scale(zone_de_texte, (200,50))
        self.screen.blit(zone_de_texte, (posx+50, posy+400))
    
    def destroy_chat(self,posx, posy):
        TRANSPARENT= (0, 0, 0, 0)
        self.rect.fill(TRANSPARENT)
        self.screen.blit(self.rect, (posx, posy))
    