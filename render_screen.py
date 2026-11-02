import pygame
import game_functions as gf
import settings as st
import text
import game_items
import enemies
import crt

import random


class Animation():

    def __init__(self, image, position, duration = 1, anim_type = "None"):

        #image to blit
        self.image = image
        #position where to blit
        self.position = position
        #ammount of frames to blit
        self.duration = duration
        #Helps with the animations
        #"enemy" animation get "movement" animation added to their movement
        self.type = anim_type
        #If the process before was done, = True
        self.adjusted = False

        #self.id = random.randrange(0,10000)

def update_dungeon(dungeon):

    
    #dungeon.game_canvas.fill(st.UISettings().bg_color)

    #dungeon.render_dungeon(tileset)
    #enemies.render_enemies(dungeon, game_canvas)
    dungeon.game_canvas.fill(st.UISettings().bg_color)
    dungeon.game_canvas.blit(dungeon.floor_tiles_canvas, (0,0))
    game_items.render_items(dungeon, dungeon.game_canvas)
    dungeon.stairs.blitme()
    dungeon.render_corpses()
    dungeon.game_canvas.blit(dungeon.walls_canvas, (0,0))

    #dungeon.game_canvas.blit(dungeon.chara.tileset.image, dungeon.chara.position, cutout)
def update_enemies(dungeon, screen):
    
    center = dungeon.chara.position

    if len(dungeon.anim_list[0])== 0:
        for enemy in dungeon.enemies:
            #print(enemy.name  + " position: " + str((enemy.position.top,enemy.position.left)))
            
            if enemy.anim_loop> 60:
                enemy.anim_loop = 1
            else:
                enemy.anim_loop +=1
            if (-4*st.GameSettings().tile_size < enemy.position.top-center.top < 8*st.GameSettings().tile_size and
                -6*st.GameSettings().tile_size < enemy.position.left-center.left < 12*st.GameSettings().tile_size):
                if enemy.anim_loop <= 30:
                    cutout = st.Tilesets().enemy_ts.tiles[enemy.id+8]
                else:
                    cutout = st.Tilesets().enemy_ts.tiles[enemy.id]
            
            
                screen.blit(st.Tilesets().enemy_ts.image, enemy.position, cutout)

def update_screen(realscreen, canvas, game_canvas, i_canvas, text_canvas,
                   chara, tileset, dungeon):
    """Update images on the screen and flip to the new screen."""
    # Redraw the screen during each pass through the loop.
    #dungeon.walls_canvas = render_dungeon_walls(dungeon)
    # ---------------- Game Canvas  -------------------:

    update_dungeon(dungeon)
    
    #chara.blitme()
    dungeon.blit_anims() 

    game_canvas.fill(st.UISettings().bg_color)
    game_canvas.blit(dungeon.game_canvas, (0,0))
    update_enemies(dungeon, game_canvas)

    chara.blitme(game_canvas)

    # ----------------- Inventory Canvas  -------------------:
    i_canvas.fill((0,0,0,0))
    update_inventory(i_canvas, chara, dungeon)
    # ----------------- Text canvas  -------------------:
    text_canvas.fill((0,0,0,0))

    update_text_canvas(text_canvas, dungeon)



    # ----------------- Canvas  -------------------:
    realscreen.fill(st.UISettings().bg_color)

    marginl = st.UISettings().mini_screen_margins_left
    marginu = st.UISettings().mini_screen_margins_up

    # We render the dungeon
    canvas.blit(game_canvas, (marginl,marginu))

    # We render the ui
    update_ui_overlay(canvas, chara)

    #NOTE: the flesh level and floor level are rendered in the floor and flesh functions

    # We render the inventory
    canvas.blit(i_canvas, st.UISettings().inventory_place)
    canvas.blit(text_canvas, st.UISettings().text_canvas_place)
    canvas.blit(dungeon.minimap_canvas, st.UISettings().minimap_place)
    canvas.blit(dungeon.super_minimap_canvas, st.UISettings().minimap_place)

    # ----------------- Cool Effects  -------------------:
    #crt.apply_crt_effect(canvas, "medium")

    # ----------------- Real Screen  -------------------:
    realscreen.blit(canvas, (0,0))

    pygame.display.flip()

def update_screen_main_menu(realscreen, menu):

    lines = menu.lines
    height_of_line = st.UISettings().text_margin_up

    realscreen.blit(menu.canvas, (0,0))
    for line in lines:
        text.render_text(realscreen, line, 
                        (st.UISettings().text_margin_left,
                        height_of_line,
                        ))
        height_of_line += st.UISettings().text_line_height

    #realscreen.blit(screen, (0,0))
    pygame.display.flip()

def update_ui_overlay(canvas, chara):
    canvas.blit(chara.black_margins, (0,0))
    canvas.blit(chara.life_bars, (0,0))

    canvas.blit(chara.life_bar_oclusor, chara.life_bar_oclusor_place)
    canvas.blit(chara.san_bar_oclusor, chara.san_bar_oclusor_place)

    canvas.blit(chara.ui_overlay, (0,0))
    canvas.blit(chara.flesh_canvas, (29,25))

    canvas.blit(chara.floor_canvas, (505,22))

    canvas.blit(chara.inventory_banner, (465, 135))

    if chara.inventory_extra_open == True:
        canvas.blit(chara.inventory_extra, 
                    (345,89+49+chara.cursor_position*st.UISettings().text_line_height))

def update_text_canvas_alt(text_canvas, dungeon, chara):

    if len(dungeon.events)>3:
        for i in range(1, 4):
            text.render_text(text_canvas, dungeon.events[-i],
                            (0, i*st.GameSettings().tile_size)
                            )

def update_text_canvas(canvas, dungeon):
    canvas.blit(dungeon.events_canvas, (0,0))

def render_text_canvas(dungeon):
    fake_canvas = pygame.Surface((422,86), pygame.SRCALPHA)
    fake_canvas.fill((0,0,0,0)) 

    if len(dungeon.events)<4:
        for i in range(1,len(dungeon.events)+1):
            text.render_text(fake_canvas, dungeon.events[-len(dungeon.events)+i],
                        (16, 6+(i-1)*(st.UISettings().text_box_line_height-10))
                        )
    else:
        for i in range(1,5):
            text.render_text(fake_canvas, dungeon.events[-4+i],
                        (16, 6+(i-1)*(st.UISettings().text_box_line_height-10))
                        )

    return fake_canvas

def update_inventory(i_canvas, chara, dungeon):
    if chara.inventory_page == 0:
        text.render_text(i_canvas, "CONTROLS",
                         (st.GameSettings().tile_size,0))
        i_canvas.blit(chara.controls_page)
    else:
        

        i_canvas.blit(chara.inventory_canvas, (0,0))
        #render_inventory_page(i_canvas, chara)
        # Render the cursor

def render_floor_canvas(chara):
    fake_canvas = pygame.Surface((40,40), pygame.SRCALPHA)
    fake_canvas.fill((0,0,0,0)) 
    rect = fake_canvas.get_rect()
    text.render_text_small(fake_canvas, str(chara.floor), (7, 0))

    return fake_canvas

def render_flesh_canvas(chara):
    fake_canvas = pygame.Surface((24,22), pygame.SRCALPHA)
    fake_canvas.fill((0,0,0,0)) 
    rect = fake_canvas.get_rect()
    text.render_text_small(fake_canvas, str(chara.flesh), (rect.centerx-3, rect.centery-7))

    return fake_canvas

def render_controls_page():
    """Renders all the control explanations into a surface"""
    # and then returns it

    controls = ["A: Attack", "Dir: Move",
                "X: Inventory/Examine", "Y: Lock in place",
                "B+Dir: Run", "B+A: Fast forward",
                "R: Lock Diagonal"]
    fake_i_canvas = pygame.Surface(st.UISettings().i_screen_size, pygame.SRCALPHA)
    fake_i_canvas.fill((0,0,0,0))

    for i in range(len(controls)):
        text.render_text(fake_i_canvas, controls[i],
                            (st.GameSettings().tile_size,
                            (i+1)*st.UISettings().text_line_height
                            ))
    return fake_i_canvas

def render_inventory_canvas(chara):
    inventory_page = chara.inventory[(chara.inventory_page-1)*7:(chara.inventory_page)*7]

    fake_i_canvas = pygame.Surface(st.UISettings().i_screen_size, pygame.SRCALPHA)
    fake_i_canvas.fill((0,0,0,0))

    for i in range(len(inventory_page)):
            text.render_text(fake_i_canvas, chara.inventory[i].name,
                                (36,
                                49+i*st.UISettings().text_line_height
                                ))

    
    for i in range(0, 7):
        fake_i_canvas.blit(chara.cursor_void, (20,52+i*st.UISettings().text_line_height))

    text.render_text_small(fake_i_canvas, "<" + str(chara.inventory_page) + "/" + str(chara.max_pages) + ">",
                      (2*st.GameSettings().tile_size, 8*st.GameSettings().tile_size))

    if chara.inventory_open:
        fake_i_canvas.blit(chara.cursor_full,
                    (20,52+(chara.cursor_position-1)*st.UISettings().text_line_height)
                    )
    return fake_i_canvas

def render_dungeon_walls(dungeon):

    canvas = pygame.Surface(st.UISettings().mini_screen_size, pygame.SRCALPHA)
    canvas.fill((0,0,0,0))

    for key, values in dungeon.edges.items():
        for edge in values:
            edge_im_pos = pygame.Rect(edge.left,edge.top-st.GameSettings().tile_size
                                        ,st.GameSettings().tile_size,st.GameSettings().tile_size)
            canvas.blit(dungeon.tileset.image, edge_im_pos, dungeon.tileset.tiles[key])

    return canvas


def render_floor_tiles(dungeon):
    """Takes all of the floor tiles and associates some of them a sprite"""
    canvas = pygame.Surface(st.GameSettings().dungeon_dim_pixels, pygame.SRCALPHA)
    canvas.fill((0,0,0,0))

    for number, tile_list in dungeon.grass_tiles.items():
            for tile in tile_list:
                canvas.blit(dungeon.floor_tiles_tileset.image, tile,
                            dungeon.floor_tiles_tileset.tiles[number])

    return canvas

def render_inventory_extra():
    
    canvas = pygame.Surface((96,128), pygame.SRCALPHA)
    canvas.fill((0,0,0,160))

    text.render_text(canvas, "Use", (32,0) )
    text.render_text(canvas, "Info", (32,32) )
    text.render_text(canvas, "Drop", (32,64) )
    text.render_text(canvas, "Quit", (32,96) )

    return canvas

def render_minimap(dungeon):
    dungeon_dim = st.GameSettings().dungeon_dim
    tilesize = st.GameSettings().tile_size
    canvas = pygame.Surface((dungeon_dim[0]*tilesize, dungeon_dim[1]*tilesize),
                            pygame.SRCALPHA)
    
    whitesquare = pygame.Surface((32,32))
    bluesquare = whitesquare.copy()
    whitesquare.fill((255,255,255))
    bluesquare.fill((12, 137, 232))

    for tile in dungeon.tiles:

        canvas.blit(whitesquare, tile)

    canvas.blit(bluesquare, dungeon.stairs.position)


    canvas = pygame.transform.scale_by(canvas, 0.15)
    return canvas

def render_super_minimap(dungeon):

    dungeon_dim = st.GameSettings().dungeon_dim
    tilesize = st.GameSettings().tile_size
    canvas = pygame.Surface((dungeon_dim[0]*tilesize, dungeon_dim[1]*tilesize),
                            pygame.SRCALPHA)

    canvas.fill((0,0,0,0))
    
    whitesquare = pygame.Surface((32,32))
    redsquare = whitesquare.copy()
    yellowsquare = whitesquare.copy()
    greensquare = whitesquare.copy()
    redsquare.fill((212, 25, 4))
    yellowsquare.fill((250, 222, 10))
    greensquare.fill((56, 219, 11))

    for enem_pos in dungeon.enemies_positions:

        true_enem_pos = enem_pos[:]
        true_enem_pos[0] += dungeon.chara.displacement[0]
        true_enem_pos[1] += dungeon.chara.displacement[1]

        canvas.blit(redsquare, true_enem_pos)

    for item_pos in dungeon.item_positions:

        true_item_pos = item_pos[:]
        true_item_pos[0] += dungeon.chara.displacement[0]
        true_item_pos[1] += dungeon.chara.displacement[1]

        canvas.blit(greensquare, true_item_pos)

    true_chara_pos0 = dungeon.chara.realposition[0]
    true_chara_pos1 = dungeon.chara.realposition[1]
    true_chara_pos0 += dungeon.chara.displacement[0]
    true_chara_pos1 += dungeon.chara.displacement[1]

    canvas.blit(yellowsquare, (true_chara_pos0, true_chara_pos1))

    canvas = pygame.transform.scale_by(canvas, 0.15)

    return canvas

