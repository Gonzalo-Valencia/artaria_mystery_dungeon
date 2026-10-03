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

""" def run_game():
    # Make the character:
    pygame.init()
    pygame.display.set_caption("Artaria Mystery Dungeon")
    screen = st.Abstract().screen2
    chara = Chara(screen)
    running = False
    # Start the main loop for the game.
    while True:
        # Watch for keyboard and mouse events.
        for event in pygame.event.get():
            print(str(event))
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT:
                    running = False
                print("keyup")
            elif event.type == pygame.KEYDOWN:
                print("keydown")
                if event.key == pygame.K_RIGHT:
                    running = True
            elif running == True:
                chara.rect.centerx += 1

        chara.blitme()

        pygame.display.flip()


run_game() """


a = (1,2)
b = (2,3)
a = b

print(b)