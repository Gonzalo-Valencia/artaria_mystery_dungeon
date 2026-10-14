import pygame
import random
import time

import settings as st
import game_functions as gf
import text
import render_screen as rs

def update_flesh_page():
    """It updates the skills usable in the flesh page"""
    flesh_skills = ["Flesh Sword", "Blood Burst"
    ]
    #Blood burst heals you

    #Flesh sword is a sword



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

        self.tileset = st.Tilesets().chara_ts

        #Start each new character at the bottom center of the screen

        #self.rect.centerx = self.screen_rect.width/2
        #self.rect.centery = self.screen_rect.height/2

        self.rect.left = 6*st.GameSettings().tile_size
        self.rect.top = 4*st.GameSettings().tile_size

        self.locked = False
        self.running = False
        self.mov_key_pressed = False
        self.a_pressed = False
        self.inventory_open = False
        self.has_moved_this_turn = False
        self.diagonal_locked = False

        #Makes it impossible to receibe buttondown and such more than
        # 6 times per second (once every 10 frames)
        self.buffer = 0
        self.buffer_bool = False

        # Save the direction of the character as a "vector"
        self.direction = (0,1)
        # First coordinate is horizontal
        # Second is vertical
        # Follow the same logic as coordinates in screen

        # Used for automatic movement
        self.movement_counter = 0

        self.hp = 60
        self.max_hp = 60
        self.san = 100
        self.max_san = 100
        self.hp_regen = 0.25
        self.san_anti_regen = 0.25
        self.dmg = 1

        self.floor = 1
        self.floor_canvas = rs.render_floor_canvas(self)

        self.inventory = []
        self.inventory_page = 1
        self.max_pages = 3

        self.flesh = 0
        self.flesh_canvas = rs.render_flesh_canvas(self)

        self.inventory_banner = pygame.image.load(st.SpritePaths().inventory_banner_path)
        self.cursor_void = pygame.image.load(st.SpritePaths().cursor_path).convert_alpha()
        self.cursor_full = pygame.image.load(st.SpritePaths().cursor_full_path).convert_alpha()
        
        #The ui overlay is loaded just once
        self.ui_overlay = pygame.image.load(st.SpritePaths().ui_overlay_path).convert_alpha()
        #Surfaces:
        self.controls_page = rs.render_controls_page()
        self.inventory_canvas = rs.render_inventory_canvas(self)
        self.black_margins = pygame.image.load(st.SpritePaths().black_margins).convert_alpha()
        self.life_bars = pygame.image.load(st.SpritePaths().life_bars).convert_alpha()

        self.life_bar_oclusor = pygame.Surface((0, 0))
        self.life_bar_oclusor_place = (0,0)

        self.san_bar_oclusor = pygame.Surface((0, 0))
        self.san_bar_oclusor_place = (0,0)

        # In which line the cursor is (starting from 1)
        self.cursor_position = 1

    def blitme_alt(self):
        """Draw the character at its current location."""
        self.screen.blit(self.image, self.rect)

    def blitme(self, screen):
        number = self.direction[0]+1+(self.direction[1]+1)*3
        if number > 4:
            number = number-1
        elif number == 4:
            number = 6
        cutout = self.tileset.tiles[number]


        screen.blit(self.tileset.image, self.rect, cutout)

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
        corpse = self.corpse_infront(dungeon)

        if corpse != None:
            st.SFX().chara_attack.play()
            dungeon.remove_corpse(corpse)

            self.flesh += 1
            self.flesh_canvas = rs.render_flesh_canvas(self)

        if enemy != None:

            if self.direction in [(1,1), (-1,1), (1,-1), (-1,-1)]:
                if (gf.predict_next_rect((self.direction[0], 0), self.rect) in dungeon.tiles and
                    gf.predict_next_rect((0, self.direction[1]), self.rect) in dungeon.tiles):
                    self.do_damage(dungeon, enemy)
            else:
                self.do_damage(dungeon, enemy)
        else:
            dungeon.rerender_text_canvas("Chara attacked nothing!")

        self.a_pressed = True

    def do_damage(self, dungeon, enemy):
        st.SFX().chara_attack.play()
        enemy.hp -= self.dmg
        #enemy.clash(dungeon, self)
        dungeon.rerender_text_canvas("Chara dealt "+ str(self.dmg) + " to the " + enemy.name + "!")


    def enemy_infront(self, dungeon):
            charadir = self.direction
            charapos = self.rect
            newrect = gf.predict_next_rect(charadir, charapos)

            enemy = dungeon.rect_to_enemy(newrect)

            return enemy

    def corpse_infront(self, dungeon):
            newrect = gf.predict_next_rect(self.direction, self.rect)

            corpse = dungeon.rect_to_corpse(newrect) 

            return corpse      

    def use_item(self, dungeon):

        if self.cursor_position <= len(self.inventory):
            st.SFX().menu_select.play()
            item = self.inventory.pop(self.cursor_position-1)
            print(item.name + " used!")
            item.items_use(self, dungeon)
            self.inventory_canvas = rs.render_inventory_canvas(self)

    def in_danger(self, dungeon):

        vicinity = gf.get_vicinity(self.rect)
        vicinity.append(self.rect)

        nextrect = gf.predict_next_rect(self.direction, self.rect)
        next_vicinity = gf.get_vicinity(nextrect)
        next_vicinity.append(nextrect)

        #If theres an enemy close
        if [rect for rect in dungeon.enemies_positions if rect in next_vicinity]:
            return True
        #Or the stairs
        if dungeon.stairs.position in next_vicinity:
            return True
        #Or an item
        if [rect for rect in dungeon.item_positions if rect in next_vicinity]:
            return True
        if nextrect in dungeon.edges_list:
            return True

        if self.direction == (-1,0):
            #If youre moving left

            #And you coud turn up or down
            if ((vicinity[2] in dungeon.edges_list and
                vicinity[1] in dungeon.tiles) or 
                (vicinity[7] in dungeon.edges_list and
                 vicinity[6] in dungeon.tiles)
                ):           
                return True
        elif self.direction == (-1,0):
            if ((vicinity[0] in dungeon.edges_list and
                vicinity[1] in dungeon.tiles) or 
                (vicinity[5] in dungeon.edges_list and
                 vicinity[6] in dungeon.tiles)
                ):               
                return True
        elif self.direction == (0,-1):
            if ((vicinity[5] in dungeon.edges_list and
                vicinity[3] in dungeon.tiles) or 
                (vicinity[7] in dungeon.edges_list and
                 vicinity[4] in dungeon.tiles)
                ):   
                return True
        elif self.direction == (0,1):
            if ((vicinity[0] in dungeon.edges_list and
                vicinity[3] in dungeon.tiles) or 
                (vicinity[2] in dungeon.edges_list and
                 vicinity[4] in dungeon.tiles)
                ):         
                return True
        
        
        return False
        


    

        