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

        self.locked = False
        self.running = False
        self.mov_key_pressed = False
        self.a_pressed = False
        self.inventory_open = False

        # Save the direction of the character as a "vector"
        self.direction = pygame.K_DOWN
        # First coordinate is horizontal
        # Second is vertical
        # Follow the same logic as coordinates in screen

        self.hp = 60
        self.max_hp = 60
        self.san = 100
        self.max_san = 100
        self.hp_regen = 0.25
        self.san_anti_regen = 0.25
        self.dmg = 1
        self.floor = 1

        self.inventory = []
        self.inventory_page = 1
        self.max_pages = 3

        self.flesh = 0

        #The ui overlay is loaded just once
        self.ui_overlay = pygame.image.load(st.SpritePaths().ui_overlay_path).convert_alpha()

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
        corpse = self.corpse_infornt(dungeon)

        message = "Chara: Attacked"

        if corpse != None:
            st.SFX().chara_attack.play()
            dungeon.remove_corpse(corpse)

            self.flesh += 1

        if enemy != None:
            st.SFX().chara_attack.play()
            enemy.hp -= self.dmg
            #enemy.clash(dungeon, self)

            dungeon.events.append("Chara dealt "+ str(self.dmg) + " to the " + enemy.name + "!")
            print("Enemy hp: " + str(enemy.hp))

        self.a_pressed = True

    def enemy_infront(self, dungeon):
            charadir = self.direction
            charapos = self.rect
            newrect = gf.predict_next_rect(charadir, charapos)

            enemy = dungeon.rect_to_enemy(newrect)

            return enemy

    def corpse_infornt(self, dungeon):
            newrect = gf.predict_next_rect(self.direction, self.rect)

            corpse = dungeon.rect_to_corpse(newrect) 

            return corpse      

    def use_item(self, dungeon):

        if self.cursor_position <= len(self.inventory):
            st.SFX().menu_select.play()
            item = self.inventory.pop(self.cursor_position-1)
            print(item.name + " used!")
            item.items_use(self, dungeon)

    def in_danger(self, dungeon):

        vicinity = gf.get_vicinity(self.rect)
        vicinity.append(self.rect)

        nextrect = gf.predict_next_rect(self.direction, self.rect)
        next_vicinity = gf.get_vicinity(nextrect)
        next_vicinity.append(nextrect)

        #If theres an enemy close
        if [rect for rect in dungeon.enemies_positions if rect in next_vicinity]:
            print("ENEMY!")
            return True
        #Or the stairs
        if dungeon.stairs.position in next_vicinity:
            print("STAIRS!")
            return True
        #Or an item
        if [rect for rect in dungeon.item_positions if rect in next_vicinity]:
            print("ITEM!")
            return True
        #Or if you're about to turn
        walk_squares_now = [rect for rect in dungeon.tiles if rect in vicinity]
        walk_squares_next = [rect for rect in dungeon.tiles if rect in next_vicinity]

        if nextrect in dungeon.edges_list:
            print("WALL IN FRONT!")
            return True

        if self.direction == pygame.K_LEFT:
            #If youre moving left

            #And you coud turn up or down
            if ((vicinity[2] in dungeon.edges_list and
                vicinity[1] in dungeon.tiles) or 
                (vicinity[7] in dungeon.edges_list and
                 vicinity[6] in dungeon.tiles)
                ):
                print("TURN")             
                return True
        elif self.direction == pygame.K_RIGHT:
            if ((vicinity[0] in dungeon.edges_list and
                vicinity[1] in dungeon.tiles) or 
                (vicinity[5] in dungeon.edges_list and
                 vicinity[6] in dungeon.tiles)
                ):             
                print("TURN")      
                return True
        elif self.direction == pygame.K_UP:
            if ((vicinity[5] in dungeon.edges_list and
                vicinity[3] in dungeon.tiles) or 
                (vicinity[7] in dungeon.edges_list and
                 vicinity[4] in dungeon.tiles)
                ):
                print("TURN")      
                return True
        elif self.direction == pygame.K_DOWN:
            if ((vicinity[0] in dungeon.edges_list and
                vicinity[3] in dungeon.tiles) or 
                (vicinity[2] in dungeon.edges_list and
                 vicinity[4] in dungeon.tiles)
                ):
                print("TURN")              
                return True
        
        
        return False
        


    

        