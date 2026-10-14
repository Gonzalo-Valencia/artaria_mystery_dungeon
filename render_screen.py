import pygame
import game_functions as gf
import settings as st
import text
import game_items
import enemies


class Animation():

    def __init__(self, image, position, duration = 0):

        #image to blit
        self.image = image
        #position where to blit
        self.position = position
        #ammount of frames to blit
        self.duration = duration


def update_dungeon(screen, dungeon, tileset):

    center = dungeon.chara.rect
    #render enemies
    #ONly if they can be seen
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
            #screen.blit(dungeon.placeholder, enemy.position)

        """for edge in dungeon.edges_list:
        if (enemy.position.top < 8*st.GameSettings().tile_size and
                    enemy.position.top > -4*st.GameSettings().tile_size and
                    enemy.position.left < 12*st.GameSettings().tile_size and
                    enemy.position.left > -6*st.GameSettings().tile_size):
            dungeon.screen.blit(tileset.image, edge, tileset.tiles[0]) """

    screen.blit(dungeon.walls_canvas, (0,0))

    """     number = dungeon.chara.direction[0]+1+(dungeon.chara.direction[1]+1)*3
    if number > 4:
        number = number-1
    elif number == 4:
        number = 6
    cutout = dungeon.chara.tileset.tiles[number] """


    #dungeon.game_canvas.blit(dungeon.chara.tileset.image, dungeon.chara.rect, cutout)


def update_screen(realscreen, canvas, game_canvas, i_canvas, text_canvas,
                   chara, tileset, dungeon):
    """Update images on the screen and flip to the new screen."""
    # Redraw the screen during each pass through the loop.
    #dungeon.walls_canvas = render_dungeon_walls(dungeon)
    # ---------------- Game Canvas  -------------------:
    dungeon.game_canvas.fill(st.UISettings().bg_color)

    #dungeon.render_dungeon(tileset)
    game_items.render_items(dungeon, dungeon.game_canvas)
    dungeon.stairs.blitme()
    dungeon.render_corpses()
    #enemies.render_enemies(dungeon, game_canvas)
    update_dungeon(dungeon.game_canvas, dungeon, tileset)
    #chara.blitme()
    dungeon.blit_anims() 

    game_canvas.fill(st.UISettings().bg_color)
    game_canvas.blit(dungeon.game_canvas, (0,0))

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

    # We render the inventory
    canvas.blit(i_canvas, st.UISettings().inventory_place)
    canvas.blit(text_canvas, st.UISettings().text_canvas_place)


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

    canvas.blit(chara.floor_canvas, (505,26))

    canvas.blit(chara.inventory_banner, (465, 135))

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
                                        (16, (i-1)*(st.UISettings().text_line_height-10))
                                        )
    else:
        for i in range(1,5):
            text.render_text(fake_canvas, dungeon.events[-4+i],
                                                    (16, (i-1)*(st.UISettings().text_line_height-10))
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
    fake_canvas = pygame.Surface((40,20), pygame.SRCALPHA)
    fake_canvas.fill((0,0,0,0)) 
    rect = fake_canvas.get_rect()
    text.render_text_small(fake_canvas, str(chara.floor), (0, 0))

    return fake_canvas

def render_flesh_canvas(chara):
    fake_canvas = pygame.Surface((24,22), pygame.SRCALPHA)
    fake_canvas.fill((0,0,0,0)) 
    rect = fake_canvas.get_rect()
    text.render_text_small(fake_canvas, str(chara.flesh), (rect.centerx-2, rect.centery-5))

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