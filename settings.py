import pygame
import e_tileset

class SpritePaths():
    #All of the paths for sprites

    def __init__(self):
        self.chara_path = 'chara_sprites/chara_placeholder.bmp'
        self.bg_path = 'map_sprites/bg_placeholder.jpg'
        self.tileset_path = 'map_sprites/floor1_tileset.bmp'
        self.enemy_tileset_path = 'chara_sprites/enemies_tileset_placeholder.bmp'
        self.stairs_path = 'map_sprites/stairs_placeholder.bmp'
        self.item_path = 'chara_sprites/item_placeholder.bmp'
        self.cursor_path = 'ui_sprites/cursor_placeholder.bmp'

class UISettings():
    #Definition of all the UI settings

    def __init__(self):
        #Screen proportions
        self.screen_width = 19*64
        self.screen_height = 13*64
        self.screen_size = (self.screen_width, self.screen_height)

        self.mini_screen_width = 13*64
        self.mini_screen_height = 9*64
        self.mini_screen_size = (self.mini_screen_width,
                                 self.mini_screen_height)

        #Screen color
        self.bg_color = (20,20,20)

        #Text
        self.menu_font = pygame.font.SysFont('Times New Roman', 48)
        self.font_color = (245,245,245)
        self.text_margin_left = 64+32
        self.text_margin_up = 64
        self.text_line_height = 64

        self.mini_screen_margins_left = 48
        self.mini_screen_margins_up = 48

        self.inventory_place_left = (self.mini_screen_margins_left+
                                self.mini_screen_width + self.mini_screen_margins_left)
        self.inventory_place_up = self.mini_screen_margins_up
        self.inventory_place = (self.inventory_place_left, self.inventory_place_up)

class GameSettings():

    def __init__(self):

        self.dungeon_dim = (30, 30) #cells per map
        self.tile_size = 64
        self.mov_keys = [pygame.K_RIGHT, pygame.K_LEFT, pygame.K_UP, pygame.K_DOWN]

class ItemSettings():

    def __init__(self):

        self.item_ammount_chance = [3,4,4,5,5,5,5,6,6,7]

        self.blackfire_dmg = 4
        self.whitefire_heal = 30

class Tilesets():

    def __init__(self):

        self.enemy_ts = e_tileset.EnemyTileset()

class Abstract():

    def __init__(self):
        #self.screen = pygame.display.set_mode(UISettings().screen_size)
        #self.screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)

        #Monitor info for nice scalling:
        info = pygame.display.Info()
        monitor_width = info.current_w
        monitor_height = info.current_h

        """IMPORTANTE: si llamamos dos "display" como screens toda crashea"""
        resize = 1
        #self.screen2 = pygame.display.set_mode(
        #    (monitor_width*resize , monitor_height *resize), 
        #    pygame.SCALED | pygame.RESIZABLE | pygame.FULLSCREEN,
        #    vsync=1
        #    )
        
        #Make resize <1 to scale the image (and the window) by a factor of 1/resize

        self.screen2 = pygame.display.set_mode(
            (UISettings().screen_width *resize, UISettings().screen_height * resize), 
            pygame.SCALED | pygame.FULLSCREEN ,
            vsync=1
            )

