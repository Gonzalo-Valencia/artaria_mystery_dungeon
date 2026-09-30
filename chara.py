import pygame
import random
import time

import settings as st
import game_functions as gf
import text

class Chara():

    def __init__(self, screen):
        
        """Initialize the main character and set its starting position."""
        self.screen = screen
        self.tilesize = st.GameSettings().tile_size

        # Load the chara image and get its rect.
        #self.image = pygame.image.load(st.SpritePaths().chara_path)
        self.image = pygame.image.load(st.SpritePaths().chara_path)
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()

        #Start each new character at the bottom center of the screen
        #self.rect.centerx = self.screen_rect.centerx
        #self.rect.centery = self.screen_rect.centery
        self.rect.centerx = self.screen_rect.width/2
        self.rect.centery = self.screen_rect.height/2

        # Save the direction of the character
        self.direction = pygame.K_DOWN

        self.hp = 60
        self.dmg = 1
        self.floor = 1

        self.inventory = []

        # In which line the cursor is (starting from 1)
        self.cursor_position = 1

    def blitme(self):
        """Draw the character at its current location."""
        self.screen.blit(self.image, self.rect)

    def get_direction_vector(self) -> tuple:
        if self.direction == pygame.K_UP:
            newvect = (0,-1)
        if self.direction == pygame.K_DOWN:
            newvect = (0,1)
        if self.direction == pygame.K_RIGHT:
            newvect = (1,0)
        if self.direction == pygame.K_LEFT:
            newvect = (-1,0)

        return newvect


    def attack(self, dungeon):
        """Make the player attack"""
        enemy = self.enemy_infront(dungeon)

        print("Chara: Attacked")

        if enemy != None:
            enemy.clash(dungeon, self)

    def enemy_infront(self, dungeon):
            charadir = self.direction
            charapos = self.rect
            newrect = gf.predict_next_rect(charadir, charapos)

            enemy = dungeon.rect_to_enemy(newrect)

            return enemy

    def render_inventory(self, screen):

        for i in range(len(self.inventory)):
            text.render_text(screen, self.inventory[i].name,
                             (st.GameSettings().tile_size,
                              i*st.UISettings().text_line_height
                              ))



    def use_item(self, dungeon):

        if self.cursor_position <= len(self.inventory):
            item = self.inventory.pop(self.cursor_position-1)
            print(item.name + " used!")
            item.items_use(self, dungeon)



    

        