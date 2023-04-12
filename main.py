import pygame as pg
import backup_game
from events.event_manager import EventManager
from game.game import Game
from menu import Menu
from game.textures import Textures
from Online.player import Player
from compet_mode import Comp_mode
import os, subprocess

def main():
    os.chdir('Online')
    subprocess.run(["gcc",  "-c", "-fPIC", "recv.c"])
    subprocess.run(["gcc",  "-c", "-fPIC", "send.c"])
    subprocess.run(["gcc", "-shared", "-fPIC", "-o", "libNetwork.so", "recv.o", "send.o"])
    subprocess.run(["gcc",  "-c", "-fPIC", "ip.c"])
    subprocess.run(["gcc", "-shared", "-fPIC", "-o", "libPlayer.so", "ip.o"])
    os.chdir('..')
    is_game_run = True
    is_playing = True

    pg.init()
    screen = pg.display.set_mode((1920, 1080), pg.FULLSCREEN)
    pg.display.set_caption("Taboule Raza")
    pg.display.set_icon(pg.image.load('assets/menu_sprites/game_icon.png'))
    curseur = pg.cursors.Cursor((0, 0), pg.image.load("assets/C3_sprites/system/Arrow.png"))
    pg.mouse.set_cursor(curseur)
    pg.event.set_grab(True)
    menu = Menu(screen)
   
    Textures.init(screen)

    while menu.is_active():
        menu.run()

    # Clear buttons from the menu
    EventManager.reset()
    #print(menu.get_online)
    p = None
    if menu.get_online():

        roomInformations = menu.getInformationsRoom()
        username=roomInformations["username"]
        p = Player()
        p.set_username(username)

        if menu.get_room() is not None:
            print(menu.get_room().id)
            menu.get_room().addMySelf(p)

    game = Game(screen, p, Comp_mode.get_instance(), online=menu.get_online(), room=menu.get_room(), multiplayer=menu.get_multiplayer())

    #game = Game(screen, menu.get_multiplayer())

    # Save load, need to be here to load save after init game
    if menu.get_save_loading():
        backup_game.load_game("save.bin")



    while is_game_run:

        while is_playing:

            game.run()



if __name__ == "__main__":
    main()
