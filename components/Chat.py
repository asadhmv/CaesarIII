import pygame as pg

from components.input_text import Input_text
from components.text import Text
from events.event_manager import EventManager

class Chat:
    def __init__(self,screen, posx, posy):
        self.chat_window = None
        self.entry = None
        self.send_button = None
        self.screen = screen
        self.rect = pg.Surface((300, 600), pg.SRCALPHA, 32)
        zone_de_texte= pg.image.load("assets/C3_sprites/C3/zone_msg.png")
        zone_de_texte= pg.transform.scale(zone_de_texte, (200,50))
        self.legende= Text("Send message..", 20, (posx+50, posy+360), (0,0,0))
        self.typeText = Text("", 24, (posx+50, posy+410), (0,0,0))
        self.input_message = Input_text((posx+50, posy+400), self.legende, zone_de_texte, self.typeText)
    def show_chat(self, posx, posy):
        
        self.rect.fill((255, 255, 255))
        self.screen.blit(self.rect, (posx, posy))

        self.input_message.add_input_listener()
        self.input_message.display(self.screen)
        
        
    def destroy_chat(self,posx, posy):
        TRANSPARENT= (0, 0, 0, 0)
        self.rect.fill(TRANSPARENT)
        self.screen.blit(self.rect, (posx, posy))
    