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
        self.posx = posx
        self.posy = posy
        self.rect = pg.Surface((300, 600), pg.SRCALPHA, 32)
        zone_de_texte= pg.image.load("assets/C3_sprites/C3/zone_msg.png")
        zone_de_texte= pg.transform.scale(zone_de_texte, (200,50))
        self.legende= Text("Send message..", 10, (posx+50, posy+390), (0,0,0))
        self.typeText = Text("", 24, (posx+50, posy+410), (0,0,0))
        self.input_message = Input_text((posx+50, posy+400), self.legende, zone_de_texte, self.typeText)
        
    def show_chat(self, posx, posy):
        
        self.rect.fill((255, 255, 255))
        self.screen.blit(self.rect, (posx, posy))

        self.input_message.add_input_listener()
        self.input_message.display(self.screen)
        for event in pg.event.get():
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_RETURN:
                    self.on_key_down(event)
        
    def destroy_chat(self,posx, posy):
        TRANSPARENT= (0, 0, 0, 0)
        self.rect.fill(TRANSPARENT)
        self.screen.blit(self.rect, (posx, posy))

    def on_key_down(self, event):
        if event.key == pg.K_RETURN:
            if self.typeText.pos[1] - 30 < self.posy:
                erase_surface = pg.Surface((20, 20), pg.SRCALPHA, 32)
                erase_surface.fill((0,0,0,0))
                self.screen.blit(erase_surface, self.typeText.pos)
                print(self.typeText.pos)
            self.typeText.pos = (self.typeText.pos[0], self.typeText.pos[1] - 30)

            