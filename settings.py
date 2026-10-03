import pygame
import e_tileset

class SpritePaths():
    #All of the paths for sprites

    def __init__(self):
        self.chara_path = 'creature_sprites/chara.bmp'
        self.bg_path = 'map_sprites/bg_placeholder.jpg'
        self.tileset_path = 'map_sprites/demo_tileset.bmp'
        self.enemy_tileset_path = 'creature_sprites/enemies_demo.bmp'
        self.stairs_path = 'map_sprites/stairs.bmp'
        self.item_path = 'creature_sprites/corpse.bmp'
        self.cursor_path = 'ui_sprites/cursor_placeholder.bmp'
        self.ui_overlay_path = 'ui_sprites/ui_overlay_placeholder.png'

class UISettings():
    #Definition of all the UI settings

    def __init__(self):
        #Screen proportions
        self.screen_width = 19*GameSettings().tile_size
        self.screen_height = 13*GameSettings().tile_size
        self.screen_size = (self.screen_width, self.screen_height)

        self.mini_screen_width = 13*GameSettings().tile_size
        self.mini_screen_height = 9*GameSettings().tile_size
        self.mini_screen_size = (self.mini_screen_width,
                                 self.mini_screen_height)

        self.i_screen_size = (4*32+8, 9*32)

        #Screen color
        self.bg_color = (0,0,0)

        #Text
        self.menu_font = pygame.font.SysFont('Times New Roman', 10)
        self.small_font = pygame.font.SysFont('Times New Roman', 10)
        self.font_color = (245,245,245)
        self.text_margin_left = GameSettings().tile_size+16
        self.text_margin_up = GameSettings().tile_size
        self.text_line_height = GameSettings().tile_size

        self.mini_screen_margins_left = 16
        self.mini_screen_margins_up = 16

        self.inventory_place_left = (self.mini_screen_margins_left+self.mini_screen_margins_left+
                                self.mini_screen_width)
        self.inventory_place_up = 4*GameSettings().tile_size
        self.inventory_place = (self.inventory_place_left, self.inventory_place_up)

        self.text_canvas_place = (self.mini_screen_margins_left,
                                  self.mini_screen_margins_up*2 +
                                  self.mini_screen_height-GameSettings().tile_size)


class SFX():

    def __init__(self):

        self.chara_attack = pygame.mixer.Sound("sfx/chara_attack.wav")
        self.chara_death = pygame.mixer.Sound("sfx/chara_death.wav")
        self.chara_attacked = pygame.mixer.Sound("sfx/chara_attacked.wav")
        self.enemy_death = pygame.mixer.Sound("sfx/enemy_death.wav")
        self.menu_change = pygame.mixer.Sound("sfx/menu_change.wav")
        self.menu_select = pygame.mixer.Sound("sfx/menu_select.wav")


class GameSettings():

    def __init__(self):

        self.dungeon_dim = (30, 30) #cells per map
        self.tile_size = 32
        self.mov_keys = [pygame.K_RIGHT, pygame.K_LEFT, pygame.K_UP, pygame.K_DOWN]

        self.act_keys = self.mov_keys + [pygame.K_k, pygame.K_a]

        self.max_inventory_lines = 7

class ItemSettings():

    def __init__(self):

        self.item_ammount_chance = [3,4,4,5,5,5,5,6,6,7]

        self.blackfire_dmg = 4
        self.whitefire_heal = 30
        self.flower_san_heal = 30

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

