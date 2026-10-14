import sys
import pygame

import settings as st
from chara import Chara
from background import Background
#from tileset import Tileset
from dungeon import Dungeon
from enemies import generate_enemies
import game_functions as gf
import text
import render_screen as rs
import menu

def run_game(clock, realscreen, canvas, game_canvas, i_canvas, text_canvas):
    # Make the character:
    chara = Chara(game_canvas)
    # Make the background
    bg = Background(game_canvas)
    # Make tileset
    #tileset = Tileset()
    tileset = st.Tilesets().dungeon_ts
    # Make dungeon
    dungeon = Dungeon(game_canvas, chara)

    dungeon.recenter_dg(chara)
    
    gameover = False
    # Start the main loop for the game.
    while gf.check_gameover(chara) == False:
        print(int(clock.get_fps()))

        dungeon.dt = 60/clock.get_fps()

        rs.update_screen(realscreen, canvas, game_canvas, i_canvas, text_canvas, 
                         chara, tileset, dungeon)
        # Watch for keyboard and mouse events.
        if len(dungeon.anim_list[0]) == 0:
            gf.check_events(dungeon, chara)

        clock.tick(120)

    game_over(clock, realscreen, canvas, game_canvas, i_canvas, text_canvas)

def game_over(clock, realscreen, canvas, game_canvas, i_canvas, text_canvas):
    clock.tick(st.Abstract().fps)
    print("do you wish to continue? any key=yes")
    gameover = True
    #while gameover == True:
        #if gf.check_events_menu() == True:
        #    gameover = False

    run_game(clock, realscreen, canvas, game_canvas, i_canvas, text_canvas)

def main_menu(clock, realscreen, canvas, game_canvas, i_canvas, text_canvas):
    clock.tick(st.Abstract().fps)

    menu_thing = menu.Menu()
    menu_thing.lines = ["Game Start", "Controls", "Quit"]


    inmenu = True
    while menu_thing.run_game == False:
        #print(int(clock.get_fps()))
        gf.check_events_menu(menu_thing)
        rs.update_screen_main_menu(realscreen, menu_thing)
        clock.tick(60)


    run_game(clock, realscreen, canvas, game_canvas, i_canvas, text_canvas)

# Initialize game and create a screen object.
pygame.init()
pygame.font.init()
pygame.joystick.init()
clock = pygame.time.Clock()

joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]
print(joysticks)


pygame.display.set_caption("Artaria Mystery Dungeon")

#Surface of the game: the main window
realscreen = st.Abstract().screen2

#Canvas where everything will blit
canvas = pygame.Surface(st.UISettings().screen_size, pygame.SRCALPHA)
#where the dungeon will blit
game_canvas = pygame.Surface(st.UISettings().mini_screen_size, pygame.SRCALPHA)
# Inventory canvas
i_canvas = pygame.Surface(st.UISettings().i_screen_size, pygame.SRCALPHA)
# Text canvas
text_canvas = pygame.Surface((422,86), pygame.SRCALPHA)

main_menu(clock, realscreen, canvas, game_canvas, i_canvas, text_canvas)

#run_game(st.Abstract().screen2)