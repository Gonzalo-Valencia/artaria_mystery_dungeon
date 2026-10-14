import sys

import pygame
import settings as st
from tileset import Tileset
import enemies
import text
import game_items
import render_screen as rs

# ------------------------- Movement -------------------

def move_any(direction, game_object):
    """Moves the object contrary to the movement of the character"""
    # i.e. moves the background, tiles, etc
    # game_object must have a rect
    if isinstance(game_object, pygame.rect.Rect):
        game_object.centerx -= direction[0]*st.GameSettings().tile_size
        game_object.centery -= direction[1]*st.GameSettings().tile_size
    else:
        game_object.rect.centerx -= direction[0]*st.GameSettings().tile_size
        game_object.rect.centery -= direction[1]*st.GameSettings().tile_size

def move_all_pre(direction, dungeon, chara):
    
    """moves all gameobjects movalbe (in dungeon.movables)"""
    """If theres no collision"""
    chara.mov_key_pressed = True
    if check_collission_future(direction, dungeon, chara.rect):
        pass
    else:
        
        for game_object in dungeon.movables:
            move_any(direction, game_object)

    return dungeon

def move_all(direction, dungeon, chara):

    create_move_anim(direction, dungeon)

    post_dungeon = move_all_pre(direction, dungeon, chara)
    dungeon.walls_canvas = rs.render_dungeon_walls(post_dungeon)

def create_move_anim(direction, dungeon):
    dx = direction[0]*st.GameSettings().tile_size
    
    dy = direction[1]*st.GameSettings().tile_size

    false_image = pygame.Surface(st.UISettings().mini_screen_size, pygame.SRCALPHA)

    false_image.blit(dungeon.game_canvas, (0,0))

    for i in range(1,6):
        tile = (-dx*i/5, -dy*i/5)

        dungeon.load_anims(false_image, tile, 3, i-1)

def create_any_move_anim(direction, game_object, dungeon):
    """Creates a movement animation of any game object"""
    dx = direction[0]*st.GameSettings().tile_size
    
    dy = direction[1]*st.GameSettings().tile_size

    image = game_object.sprite

    position = game_object.position

    for i in range(1,6):
        tile = (position.left-dx*i/5, position.right-dy*i/5)

        dungeon.load_anims(image, tile, 3, i-1)


# ------------------------- Check keys and buttons -------------------

def optimitation_function(event, dungeon, chara):

    if chara.inventory_open:
        if event.type == pygame.KEYDOWN:
            check_keydown_events_inventory(event, dungeon, chara)
        if event.type == pygame.JOYBUTTONDOWN:
            check_buttondown_events_inventory(event, dungeon, chara)
        if event.type == pygame.JOYHATMOTION:
            check_hatmotion_events_inventory(event, dungeon, chara)
    elif chara.running:
        if event.type == pygame.KEYDOWN:
            if event.key in st.GameSettings().mov_keys:
                chara.direction = keys_to_direction(event.key)
                move_all(chara.direction, dungeon, chara)
                check_outside_events(dungeon, chara)
                check_passive_events(dungeon, chara)
                chara.mov_key_pressed = True
            if event.key == pygame.K_a:
                chara.attack(dungeon)
                check_outside_events(dungeon, chara)
                check_passive_events(dungeon, chara)
                chara.a_pressed = True
        if event.type == pygame.JOYBUTTONDOWN:
            if event.button == 1:  #Attack 
                chara.attack(dungeon)
                check_outside_events(dungeon, chara)
                check_passive_events(dungeon, chara)
                chara.a_pressed = True
        if event.type == pygame.JOYHATMOTION:
            if event.value == (0,0):
                chara.mov_key_pressed = False
            else:
                chara.direction = buttons_to_direction(event.value)
                move_all(chara.direction, dungeon, chara)
                check_outside_events(dungeon, chara)
                check_passive_events(dungeon, chara)
                chara.mov_key_pressed = True
    elif event.type == pygame.KEYDOWN:
        check_keydown_events(event, dungeon, chara)
    elif event.type == pygame.JOYBUTTONDOWN:
        check_buttondown_events(event, dungeon, chara)
    elif event.type == pygame.JOYHATMOTION:
        check_joyhatmotion_events(event, dungeon, chara)

def check_events(dungeon, chara):
    """Respond to keypresses and mouse events"""

    chara.has_moved_this_turn = False
    if ((chara.running and chara.mov_key_pressed) or 
        (chara.running and chara.a_pressed)):
        check_events_running(dungeon, chara)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, dungeon, chara)
        elif event.type == pygame.JOYBUTTONUP:
            check_buttonup_events(event, dungeon, chara)
        elif (event.type == pygame.KEYDOWN or pygame.JOYBUTTONDOWN or pygame.JOYHATMOTION):
            optimitation_function(event,dungeon, chara)
    if chara.mov_key_pressed:
        if chara.direction in [(0,1),(1,0),(-1,0),(0,-1)] and chara.diagonal_locked == True:
            pass
        elif chara.has_moved_this_turn == False:
            move_all(chara.direction, dungeon, chara)
            check_outside_events(dungeon, chara)
            check_passive_events(dungeon, chara)
        """             if chara.movement_counter >= 14:
                move_all(chara.direction, dungeon, chara)
                check_outside_events(dungeon, chara)
                check_passive_events(dungeon, chara)
                chara.movement_counter = 0
            else:
                chara.movement_counter += 1 """

def check_keyup_events(event, dungeon, chara):
    if event.key == pygame.K_y:
        chara.locked = False
    elif event.key == pygame.K_r:
        chara.running = False
    elif event.key in st.GameSettings().mov_keys:
        chara.mov_key_pressed = False
    elif event.key == pygame.K_a:
        chara.a_pressed = False
    elif event.key == pygame.K_t:
        chara.diagonal_locked = False

def check_buttonup_events(event, dungeon, chara):
    if event.button == 2:
        chara.locked = False
    elif event.button == 0:
        chara.running = False
    elif event.button == 1:
        chara.a_pressed = False
    elif event.button == 5:
        chara.diagonal_locked = False
    elif event.button in st.GameSettings().mov_buttons:
        chara.mov_key_pressed = False

def check_keydown_events(event, dungeon, chara):
    """Respond to keypresses."""

    # First checks if the key is active or meta
    # Active keys are the ones that let you act
    # Meta are the ones that control inventory, etc
    if (event.key in st.GameSettings().act_keys 
        and chara.locked == False):
        check_active_events(event, dungeon, chara)

        direct_value = abs(chara.direction[0])+abs(chara.direction[1])
        if chara.diagonal_locked and direct_value != 2:
            pass
        else:
            check_outside_events(dungeon, chara)
            check_passive_events(dungeon, chara)
    elif event.key in st.GameSettings().mov_keys:
        keys = pygame.key.get_pressed()
        key_list = []

        for key in st.GameSettings().mov_keys:
            if keys[key] == True:
                key_list.append(key)

        chara.direction = keys_to_direction(*key_list)
    elif event.key == pygame.K_d:
        dungeon.reset_dungeon(chara)
    elif event.key == pygame.K_ESCAPE:
        sys.exit()
    elif event.key == pygame.K_i:
        st.SFX().menu_change.play()
        if chara.cursor_position > 1:
            chara.cursor_position -= 1
    elif event.key == pygame.K_m:
        st.SFX().menu_change.play()
        if chara.cursor_position < st.GameSettings().max_inventory_lines:
            chara.cursor_position += 1
    elif event.key == pygame.K_y:
        chara.locked = True
    elif event.key == pygame.K_r:
        chara.running = True
    elif event.key == pygame.K_p:
        chara.inventory_open = True
        chara.inventory_canvas = rs.render_inventory_canvas(chara)
    elif event.key == pygame.K_t:
        chara.diagonal_locked = True

def check_buttondown_events(event, dungeon, chara):
    if event.button == 1:
        chara.attack(dungeon)
        check_outside_events(dungeon, chara)
        check_passive_events(dungeon, chara)
    elif event.button == 2:
        chara.locked = True
    elif event.button == 0:
        chara.running = True
    elif event.button == 3:
        chara.inventory_open = True
        chara.inventory_canvas = rs.render_inventory_canvas(chara)
    elif event.button == 5:
        chara.diagonal_locked = True

def check_joyhatmotion_events(event, dungeon, chara):

    if event.value == (0,0):
        chara.mov_key_pressed = False
    
    elif chara.locked == True:
        chara.direction = buttons_to_direction(event.value)
    else:
        chara.mov_key_pressed = True
        if chara.has_moved_this_turn != True:
            chara.has_moved_this_turn = True

            chara.direction = buttons_to_direction(event.value)
            direct_value = abs(chara.direction[0])+abs(chara.direction[1])
            if chara.diagonal_locked and direct_value != 2:
                pass
            else:
                move_all(chara.direction, dungeon, chara)
                check_outside_events(dungeon, chara)
                check_passive_events(dungeon, chara)

def check_keydown_events_inventory(event, dungeon, chara):

    if event.key == pygame.K_RIGHT:
        if chara.inventory_page == chara.max_pages:
            chara.inventory_page = 0
        else:
            chara.inventory_page += 1
    if event.key == pygame.K_LEFT:
        if chara.inventory_page == 0:
            chara.inventory_page = chara.max_pages
        else:
            chara.inventory_page -= 1
    if event.key == pygame.K_UP:
        st.SFX().menu_change.play()
        if chara.cursor_position > 1:
            chara.cursor_position -= 1
        else:
            chara.cursor_position = st.GameSettings().max_inventory_lines
    if event.key == pygame.K_DOWN:
        st.SFX().menu_change.play()
        if chara.cursor_position < st.GameSettings().max_inventory_lines:
            chara.cursor_position += 1
        else:
            chara.cursor_position = 1
    elif event.key == pygame.K_ESCAPE or event.key == pygame.K_p:
        chara.inventory_open = False

    chara.inventory_canvas = rs.render_inventory_canvas(chara)

def check_buttondown_events_inventory(event, dungeon, chara):

    if event.button == 0:
        chara.inventory_open = False
    if event.button == 1:
        chara.use_item(dungeon)
        check_outside_events(dungeon, chara)
        check_passive_events(dungeon, chara)
    
    chara.inventory_canvas = rs.render_inventory_canvas(chara)

def check_hatmotion_events_inventory(event,dungeon, chara):


    if event.value[0] == -1:
        if chara.inventory_page == 0:
            chara.inventory_page = chara.max_pages
        else:
            chara.inventory_page -= 1
    if event.value[0] == 1:
        if chara.inventory_page == chara.max_pages:
            chara.inventory_page = 0
        else:
            chara.inventory_page += 1
    if event.value[1] == 1:
        st.SFX().menu_change.play()
        if chara.cursor_position > 1:
            chara.cursor_position -= 1
        else:
            chara.cursor_position = st.GameSettings().max_inventory_lines
    if event.value[1] == -1:
        st.SFX().menu_change.play()
        if chara.cursor_position < st.GameSettings().max_inventory_lines:
            chara.cursor_position += 1
        else:
            chara.cursor_position = 1

    chara.inventory_canvas = rs.render_inventory_canvas(chara)

def check_events_running(dungeon, chara):
    if chara.in_danger(dungeon) == False and chara.mov_key_pressed == True:
        move_all(chara.direction, dungeon, chara)
        check_outside_events(dungeon, chara)
        check_passive_events(dungeon, chara)
    elif chara.in_danger(dungeon) == False and chara.a_pressed == True:
        check_outside_events(dungeon, chara)
        check_passive_events(dungeon, chara) 



# ------------------------- Events -------------------

def check_active_events(event, dungeon, chara):
    """Checks all chara actions that move the world too"""


    if (event.key in st.GameSettings().mov_keys and 
        chara.has_moved_this_turn != True):
        chara.has_moved_this_turn = True
        # First we check if there's two keys mov keys
        # Pressed at the same time

        # This is a dict "keys[K_DOWN]: True, etc"
        keys = pygame.key.get_pressed()
        key_list = []

        for key in st.GameSettings().mov_keys:
            if keys[key] == True:
                key_list.append(key)

        chara.direction = keys_to_direction(*key_list)
        direct_value = abs(chara.direction[0])+abs(chara.direction[1])

        if chara.diagonal_locked and direct_value != 2:
            pass
        elif direct_value == 0:
            pass
        else:
            move_all(chara.direction, dungeon, chara)
    elif event.key == pygame.K_k:
        chara.use_item(dungeon)
    elif event.key == pygame.K_a:
        chara.attack(dungeon)

def check_passive_events(dungeon, chara):
    """Checks all the meta events that have to do with the chara"""
    chara.hp += chara.hp_regen
    chara.san -= chara.san_anti_regen

    if chara.hp > chara.max_hp:
        chara.hp = chara.max_hp

    chara.life_bar_oclusor = pygame.Surface((int(372*(1-chara.hp/chara.max_hp)), 22))
    chara.life_bar_oclusor_place = (int(58+372*(chara.hp/chara.max_hp)), 24)

    chara.san_bar_oclusor = pygame.Surface((int(108*(1-chara.san/chara.max_san)), 6))
    chara.san_bar_oclusor_place = (int(322+108*(chara.san/chara.max_san)), 50)

    if chara.san > chara.max_san:
        chara.san = chara.max_san

    if chara.rect in dungeon.item_positions:
        item = dungeon.rect_to_item(chara.rect)
        chara.inventory.append(item)
        chara.inventory_canvas = rs.render_inventory_canvas(chara)

        dungeon.remove_item(item)

    if chara.rect == dungeon.stairs.position:
        dungeon.reset_dungeon(chara)
        chara.floor += 1
        chara.floor_canvas = rs.render_floor_canvas(chara)

def check_outside_events(dungeon, chara):
    """Checks all events that dont have to do with the player"""

    for enemy in dungeon.enemies:
        if enemy.poisoned:
            enemy.hp -= st.ItemSettings().rot_dmg
            
        if enemy.hp <= 0:
            dungeon.remove_enemy(enemy)
        else:
            enemy.act(dungeon, chara)

    if chara.hp <= 0 or chara.san <= 0:
        st.SFX().chara_death.play()
        print("game over!")
        return True
    else:
        return False

# ------------------------- Different Screen -------------------
def check_events_menu(menu):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if (event.key == pygame.K_KP_ENTER or
                event.key == pygame.K_z or
                event.key == pygame.K_SPACE or
                event.key == pygame.K_RETURN
                ):
                menu.run_game = True

def check_gameover(chara):
    if chara.hp <= 0 or chara.san <= 0:
        st.SFX().chara_death.play()
        print("game over!")
        return True
    else:
        return False
        
# ------------------------- Useful functions -------------------

def controller_translator(event):
    if event.button == 0:
        return pygame.K_r
    if event.button == 1:
        return pygame.K_a
    if event.button == 2:
            return pygame.K_r
    if event.button == 3:
            return pygame.K_a
    if event.button == 5:
            return pygame.K_r
    if event.button == 1:
            return pygame.K_a

def get_vicinity(rect) -> list:

    """Given a rectangle it returns all the rectangles around"""
    # Without itself

    ts = st.GameSettings().tile_size

    #C = corner, u= upper, l= left, d=down, r= right
    cul = pygame.Rect(rect.left-ts, rect.top-ts, ts, ts)
    cur = pygame.Rect(rect.left+ts, rect.top-ts, ts, ts)
    cdl = pygame.Rect(rect.left-ts, rect.top+ts, ts, ts)
    cdr = pygame.Rect(rect.left+ts, rect.top+ts, ts, ts)

    #W = wall
    wu = pygame.Rect(rect.left, rect.top-ts, ts, ts)
    wd = pygame.Rect(rect.left, rect.top+ts, ts, ts)
    wl = pygame.Rect(rect.left-ts, rect.top, ts, ts)
    wr = pygame.Rect(rect.left+ts, rect.top, ts, ts)

    #These are all the squares around the rect
    return [cul, wu, cur, wl, wr, cdl, wd, cdr]

def invert_direction(direction):
    return (-direction[0], -direction[1])

def keys_to_direction(*keys):
    left = 0
    top = 0
    for key in keys:
        direction = key_to_direction(key)
        left += direction[0]
        top += direction[1]
    return (left,top)

def key_to_direction(key):
    """Converts a key pressed to a direction"""
    if key == pygame.K_RIGHT:
        return (1,0)
    if key == pygame.K_LEFT:
        return (-1,0)
    if key == pygame.K_UP:
        return (0,-1)
    if key == pygame.K_DOWN:
        return (0,1)

def buttons_to_direction(value):
    return (value[0], -value[1])

def abs_distance(rect1, rect2):
    return (abs(rect1.centerx-rect2.centerx) +
                abs(rect1.centery-rect2.centery))

def predict_next_rect(direction, rect):
    """Predicts the next square given a direction as a key"""
    newleft = rect.left
    newtop = rect.top
    tilesize = st.GameSettings().tile_size

    newleft += direction[0]*tilesize
    newtop += direction[1]*tilesize

    newrect = pygame.Rect(newleft, newtop, tilesize, tilesize)

    return newrect

def check_collission_future(direction, dungeon, rect):
        """Checks collission given a direction"""
        collisionables = (dungeon.enemies_positions + [dungeon.chara.rect] +
                          dungeon.corpses_positions
                          )
        nextrect = predict_next_rect(direction, rect)

        if nextrect in dungeon.tiles:
            if direction in [(1,1),(-1,1),(1,-1),(-1,-1)]:
                if (nextrect not in collisionables and
                    #predict_next_rect((direction[0],0), rect) not in collisionables and
                    #predict_next_rect((0,direction[1]), rect) not in collisionables and
                    predict_next_rect((direction[0],0), rect) in dungeon.tiles and
                    predict_next_rect((0,direction[1]), rect) in dungeon.tiles
                    ):
                    return False
                else:
                    return True
            elif nextrect not in collisionables:
                return False
            else:
                return True
        else:
            return True

def get_squares_in_front(direction, dungeon, rect):
    """Returns all rects in the direction, from rect, until collision"""
    tiles = []
    collision = False
    current_rect = rect
    while collision == False:
        nextrect = predict_next_rect(direction, current_rect)
        if nextrect in dungeon.tiles:
            current_rect = nextrect
            tiles.append(current_rect)
        else:
            collision = True
    return tiles


def find_closest(center, *rects):
    """Finds the closest rect to center from all rects"""
    if len(rects) > 0:
        distance = 100000
        closest_rect = rects[0]
        for rect in rects:
            this_distance = abs_distance(center,rect)
            if this_distance < distance:
                distance = this_distance
                closest_rect = rect

        return closest_rect
    else:
        return center