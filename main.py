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

def run_game(screen, realscreen, i_canvas):
    # Make the character:
    chara = Chara(screen)
    # Make the background
    bg = Background(screen)
    # Make tileset
    tileset = Tileset(screen)
    # Make dungeon
    dungeon = Dungeon(screen, chara)

    dungeon.recenter_dg(chara)

    print(chara.rect.left/64)
    gameover = False
    # Start the main loop for the game.
    while gf.check_gameover(chara) == False:
        # Watch for keyboard and mouse events.
        gf.check_events(dungeon, chara)
        gf.check_passive_events(dungeon, chara)
        gf.update_screen(screen, realscreen, i_canvas, chara, tileset, dungeon)

    game_over(screen, realscreen, i_canvas)

def game_over(screen, realscreen, i_canvas):
    print("do you wish to continue? any key=yes")
    gameover = True
    while gameover == True:
        if gf.check_events_menu() == True:
            gameover = False

    run_game(screen, realscreen, i_canvas)

def main_menu(screen, realscreen, i_canvas):

    inmenu = True
    while inmenu == True:
        if gf.check_events_menu() == True:
            inmenu = False
        else:
            gf.update_screen_main_menu(screen, realscreen)

    run_game(screen, realscreen, i_canvas)

# Initialize game and create a screen object.
pygame.init()
pygame.font.init()
# The screen is the surface where everything renders
pygame.display.set_caption("Artaria Mystery Dungeon")
# Later on, we will decide the true screen. For now, its a virtual canvas
screen = st.Abstract().screen2
canvas = pygame.Surface(st.UISettings().mini_screen_size
                        )
# Inventory canvas
i_canvas = pygame.Surface((5*64, 13*64))


main_menu(canvas, screen, i_canvas)

#run_game(st.Abstract().screen2)