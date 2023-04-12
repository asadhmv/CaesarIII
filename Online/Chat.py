import pygame as pg
from components.input_text import Input_text
from components.text import Text
from events.event_manager import EventManager
from Online.multiplayer_connection import Multiplayer_connection

class Chat:
    instance=None
    def __init__(self,screen, posx, posy, multiplayer: Multiplayer_connection):
        self.screen = screen
        self.posx = posx
        self.posy = posy
        self.rect = pg.Surface((300, 600), pg.SRCALPHA, 32)
        zone_de_texte= pg.image.load("assets/C3_sprites/C3/zone_msg.png")
        zone_de_texte= pg.transform.scale(zone_de_texte, (200,50))
        self.legende= Text("Send message..", 10, (posx+50, posy+390), (0,0,0))
        self.typeText = Text("", 24, (posx+50, posy+410), (0,0,0))
        self.input_message = Input_text((posx+50, posy+400), self.legende, zone_de_texte, self.typeText)
        self.multiplayer = multiplayer
        
        self.historyOfMessages = []
        self.historyOfMessagesreceived = []
        
        #self.message_text = Text(self.multiplayer.buffer_receive, 18, (posx+50, posy+360), (0, 0, 0))
        
    def show_chat(self, posx, posy):
        
        self.rect.fill((255, 255, 255))
        self.screen.blit(self.rect, (posx, posy))
        self.input_message.add_input_listener()
        self.input_message.display(self.screen)
        i= 0
        for line in self.historyOfMessages:
            self.historyOfMessages_blit = Text(str(line), 24,(self.posx +10  , self.posy+10+i), (0,0,0))
            self.historyOfMessages_blit.display(self.screen)
            i+=20
        EventManager.register_key_listener(pg.K_RETURN,self.add_message, params = 'username')
        

    
    

    def destroy_chat(self,posx, posy):
        TRANSPARENT= (0, 0, 0, 0)
        self.rect.fill(TRANSPARENT)
        self.screen.blit(self.rect, (posx, posy))

        
    def display_received_message(self, buffer, username):
        print("hello "+buffer)
        message=buffer
        if buffer.startswith('$chat'):
            message = message.split('$chat', 1)[1].strip()
            self.add_message_received(username, message)
          

    def add_message(self, username):
        max_messages = 17 
        if len(self.historyOfMessages) > max_messages:
            self.historyOfMessages.pop(0)
        message = self.input_message.getString()
        #Multiplayer_connection.get_instance().send_specific_buffer(message)
        username = self.multiplayer.player.get_username()
        self.historyOfMessages.append(f"@{username}: {message}")
        chat_buffer = "$chat:@" + username + ": " + message
        self.multiplayer.send_specific_buffer(chat_buffer)
        self.input_message.clear_inputText()

    def add_message_received(self, message):
        if message.startswith('$chat:'):
            max_messages = 17 
            if len(self.historyOfMessages) > max_messages:
                self.historyOfMessages.pop(0)
            message = message.split('$chat:', 1)[1].strip()
            self.historyOfMessages.append(f"{message}")
    
    @staticmethod
    def get_instance(screen,posx,posy):
        if Chat.instance is None:
            Chat.instance = Chat(screen,posx,posy)
        return Chat.instance

            

            