import sys
import pygame

import settings as st
from chara import Chara
from background import Background
from tileset import Tileset
from dungeon import Dungeon
from enemies import generate_enemies
import game_functions as gf
import text
import render_screen as rs

def run_game(realscreen, canvas, game_canvas, i_canvas, text_canvas):
    # Make the character:
    chara = Chara(game_canvas)
    # Make the background
    bg = Background(game_canvas)
    # Make tileset
    tileset = Tileset(game_canvas)
    # Make dungeon
    dungeon = Dungeon(game_canvas, chara)

    dungeon.recenter_dg(chara)

    gameover = False
    # Start the main loop for the game.
    while gf.check_gameover(chara) == False:
        # Watch for keyboard and mouse events.
        gf.check_events(dungeon, chara)
        rs.update_screen(realscreen, canvas, game_canvas, i_canvas, text_canvas, 
                         chara, tileset, dungeon)

    game_over(realscreen, canvas, game_canvas, i_canvas, text_canvas)

def game_over(realscreen, canvas, game_canvas, i_canvas, text_canvas):
    print("do you wish to continue? any key=yes")
    gameover = True
    while gameover == True:
        if gf.check_events_menu() == True:
            gameover = False

    run_game(realscreen, canvas, game_canvas, i_canvas, text_canvas)

def main_menu(realscreen, canvas, game_canvas, i_canvas, text_canvas):

    inmenu = True
    while inmenu == True:
        if gf.check_events_menu() == True:
            inmenu = False
        else:
            rs.update_screen_main_menu(realscreen, canvas, game_canvas, i_canvas)

    run_game(realscreen, canvas, game_canvas, i_canvas, text_canvas)

# Initialize game and create a screen object.
pygame.init()
pygame.font.init()

pygame.display.set_caption("Artaria Mystery Dungeon")

#Surface of the game: the main window
realscreen = st.Abstract().screen2

#Canvas where everything will blit
canvas = pygame.Surface(st.UISettings().screen_size, pygame.SRCALPHA)
#where the dungeon will blit
game_canvas = pygame.Surface(st.UISettings().mini_screen_size)
# Inventory canvas
i_canvas = pygame.Surface(st.UISettings().i_screen_size)
# Text canvas
text_canvas = pygame.Surface((st.UISettings().mini_screen_width, 4*st.GameSettings().tile_size))

main_menu(realscreen, canvas, game_canvas, i_canvas, text_canvas)

#run_game(st.Abstract().screen2)