import pygame as pg
from Online.multiplayer_connection import Multiplayer_connection

from components.input_text import Input_text
from components.text import Text
from events.event_manager import EventManager

class Chat:
    def __init__(self,screen, posx, posy):
        self.screen = screen
        self.posx = posx
        self.posy = posy
        self.rect = pg.Surface((300, 600), pg.SRCALPHA, 32)
        zone_de_texte= pg.image.load("assets/C3_sprites/C3/zone_msg.png")
        zone_de_texte= pg.transform.scale(zone_de_texte, (200,50))
        self.legende= Text("Send message..", 10, (posx+50, posy+390), (0,0,0))
        self.typeText = Text("", 24, (posx+50, posy+410), (0,0,0))
        self.input_message = Input_text((posx+50, posy+400), self.legende, zone_de_texte, self.typeText)
        self.multiplayer = Multiplayer_connection(True)
        self.historyOfMessages = []
        self.historyOfMessagesreceived = []
        
        #self.message_text = Text(self.multiplayer.buffer_receive, 18, (posx+50, posy+360), (0, 0, 0))
        
    def show_chat(self, posx, posy):
        
        self.rect.fill((255, 255, 255))
        self.screen.blit(self.rect, (posx, posy))

        self.input_message.add_input_listener()
        self.input_message.display(self.screen)
        self.display_received_message()
        i= 0
        for line in self.historyOfMessages:
            self.historyOfMessages_blit = Text(str(line), 24,(self.posx +10  , self.posy+10+i), (0,0,0))
            self.historyOfMessages_blit.display(self.screen)
            i+=20
        EventManager.register_key_listener(pg.K_RETURN,self.add_message, params = 'username')
        EventManager.register_key_listener(pg.K_m,self.send)

    
    def send(self):    
        self.multiplayer.set_buffer_send("")
        self.multiplayer.buffer_send= "$chat " + self.typeText.getString()
        #self.input_message.display(self.screen)
        if(self.multiplayer.buffer_send!="$chat "):
            self.multiplayer.send()
        else:
            self.multiplayer.set_buffer_send("")

    def destroy_chat(self,posx, posy):
        TRANSPARENT= (0, 0, 0, 0)
        self.rect.fill(TRANSPARENT)
        self.screen.blit(self.rect, (posx, posy))

        
    def display_received_message(self):
        message = self.multiplayer.buffer_receive
        if self.multiplayer.buffer_receive.startswith('$chat'):
            message = message.split('$chat', 1)[1].strip()
            # message_text = Text(message, 18, (self.posx+50, self.posy+360), (0, 0, 0))
            # message_text.display(self.screen)
            self.historyOfMessagesreceived.append(self.multiplayer.buffer_receive)
            i= 0
            for line in self.historyOfMessagesreceived:
                self.historyOfMessagesreceived_blit = Text(str(line), 24,(self.posx +10  , self.posy+10+i), (0,0,0))
                self.historyOfMessagesreceived_blit.display(self.screen)
                i+=20
        
                        
    def add_message(self, username):
        message = self.input_message.getString()

        self.historyOfMessages.append(f"@{username}: {message}")
        self.input_message.clear_inputText()


            

            