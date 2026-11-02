import pygame
import e_tileset
import tileset as ts

class SpritePaths():
    #All of the paths for sprites

    def __init__(self):
        self.chara_path = 'creature_sprites/chara.bmp'
        self.bg_path = 'map_sprites/bg_placeholder.jpg'
        self.tileset_path = 'map_sprites/demo_tileset.bmp'
        self.enemy_tileset_path = 'creature_sprites/enemies_placeholder.bmp'
        self.stairs_path = 'map_sprites/stairs.bmp'
        self.item_path = 'creature_sprites/corpse.bmp'
        self.cursor_path = 'ui_sprites/cursor_void.png'
        self.ui_overlay_path = 'ui_sprites/ui_overlay.png'
        self.chara_tileset_path = 'creature_sprites/chara_tileset.bmp'
        self.fire_path = 'special_effects/fire_placeholder.bmp'
        self.black_margins = 'ui_sprites/black_margins.png'
        self.life_bars = 'ui_sprites/life_bars.png'
        self.inventory_banner_path = 'ui_sprites/inventory_banner.bmp'
        self.cursor_full_path = 'ui_sprites/cursor_full.png'
        self.dungeon_tileset_path = 'map_sprites/dungeon_tileset.png'
        self.main_menu_path = 'ui_sprites/main_menu_placeholder.bmp'
        self.floor_tiles_tileset_path = 'map_sprites/floor_tiles_tileset.bmp'

class UISettings():
    #Definition of all the UI settings

    def __init__(self):
        #Screen proportions
        self.screen_width = 19*GameSettings().tile_size
        self.screen_height = 13*GameSettings().tile_size
        self.screen_size = (self.screen_width, self.screen_height)

        self.mini_screen_width = 18*GameSettings().tile_size
        self.mini_screen_height = 12*GameSettings().tile_size
        self.mini_screen_size = (self.mini_screen_width,
                                 self.mini_screen_height)



        #Screen color
        self.bg_color = (0,0,0)

        #Text
        self.font_path_alt = "Tiny5.ttf"
        self.font_path_alt_2 = "pix32.ttf"
        self.font_path = "Perfect_DOS_VGA_437_Win.ttf"

        self.menu_font = pygame.font.Font(self.font_path, 15)
        self.small_font = pygame.font.Font(self.font_path, 16)
        self.text_box_font = pygame.font.Font(self.font_path, 10)
        self.font_color = (195,199,175)
        self.text_margin_left = GameSettings().tile_size+16
        self.text_margin_up = GameSettings().tile_size
        self.text_line_height = 30
        self.text_box_line_height = 27

        self.mini_screen_margins_left = 16
        self.mini_screen_margins_up = 16

        self.i_screen_size = (150, 278)
        #self.inventory_place_left = (self.mini_screen_margins_left+self.mini_screen_margins_left+
                                #self.mini_screen_width)
        #self.inventory_place_up = 4*GameSettings().tile_size
        self.inventory_place = (441,121)

        self.text_canvas_place = (17, 313)

        self.minimap_place = (452, 21)


class SFX():

    def __init__(self):

        self.chara_attack = pygame.mixer.Sound("sfx/chara_attack.wav")
        self.chara_death = pygame.mixer.Sound("sfx/chara_death.wav")
        self.chara_attacked = pygame.mixer.Sound("sfx/chara_attacked.wav")
        self.enemy_death = pygame.mixer.Sound("sfx/enemy_death.wav")
        self.menu_change = pygame.mixer.Sound("sfx/menu_change.wav")
        self.menu_select = pygame.mixer.Sound("sfx/menu_select.wav")
        self.pickup = pygame.mixer.Sound("sfx/pickup.wav")
        self.stairs = pygame.mixer.Sound("sfx/stairs.wav")
        self.hit_wall = pygame.mixer.Sound("sfx/hit_wall.wav")
        self.inventory_open = pygame.mixer.Sound("sfx/inventory_open.wav")

        self.attack_nothing = pygame.mixer.Sound("sfx/attack_nothing.wav")
        self.the_rot_dmg = pygame.mixer.Sound("sfx/the_rot_dmg.wav")
        self.whitefire = pygame.mixer.Sound("sfx/whitefire.wav")
        self.a_flower = pygame.mixer.Sound("sfx/a_flower.wav")
        self.the_rot = pygame.mixer.Sound("sfx/the_rot.wav")
        self.teleport = pygame.mixer.Sound("sfx/teleport.wav")

        self.soul_bind = pygame.mixer.Sound("sfx/soul_bind.wav")
        self.item_fail = pygame.mixer.Sound("sfx/item_fail.wav")
        self.inventory_close = pygame.mixer.Sound("sfx/inventory_close.wav")


class GameSettings():

    def __init__(self):

        self.dungeon_dim = (30, 30) #cells per map
        self.tile_size = 32
        self.dungeon_dim_pixels = (self.dungeon_dim[0]*self.tile_size,
                                   self.dungeon_dim[1]*self.tile_size
                                   )
        self.mov_keys = [pygame.K_RIGHT, pygame.K_LEFT, pygame.K_UP, pygame.K_DOWN]
        self.mov_buttons = [ pygame.HAT_LEFT, pygame.HAT_DOWN, pygame.HAT_LEFTDOWN,
                            pygame.HAT_UP, pygame.HAT_LEFTUP, pygame.HAT_RIGHT,
                            pygame.HAT_RIGHTDOWN, pygame.HAT_RIGHTUP]

        self.act_keys = self.mov_keys + [pygame.K_k, pygame.K_a]

        self.max_inventory_lines = 7

class ItemSettings():

    def __init__(self):

        self.item_ammount_chance = [3,4,4,5,5,5,5,6,6,7]

        self.blackfire_dmg = 4
        self.whitefire_heal = 30
        self.flower_san_heal = 30
        self.incinerate_dmg = 3
        self.rot_dmg = 1

class Tilesets():

    def __init__(self):

        self.dungeon_ts = ts.Tileset(SpritePaths().tileset_path)
        self.enemy_ts = e_tileset.EnemyTileset()
        self.chara_ts = ts.Tileset(SpritePaths().chara_tileset_path)
        self.dungeon_long_ts = ts.Long_Tileset(SpritePaths().dungeon_tileset_path)
        #4 by 4, 16 in total
        self.floor_tiles_tileset = ts.Tileset(SpritePaths().floor_tiles_tileset_path)

class Abstract():

    def __init__(self):
        #self.screen = pygame.display.set_mode(UISettings().screen_size)
        #self.screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)

        self.buffer_frames = 10

        #Monitor info for nice scalling:
        info = pygame.display.Info()
        monitor_width = info.current_w
        monitor_height = info.current_h

        self.enemy_tileset_width_tiles = 8

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

        self.fps = 60

