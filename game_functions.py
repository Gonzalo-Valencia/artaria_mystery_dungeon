import sys

import pygame
import settings as st
from tileset import Tileset
import enemies
import text
import game_items

def move_any(key, game_object):
    """Moves the object contrary to the movement of the character"""
    # i.e. moves the background, tiles, etc
    # game_object must have a rect
    if isinstance(game_object, pygame.rect.Rect):
        if key == pygame.K_RIGHT:
            game_object.centerx -= st.GameSettings().tile_size
        if key == pygame.K_LEFT:
            game_object.centerx += st.GameSettings().tile_size
        if key == pygame.K_UP:
            game_object.centery += st.GameSettings().tile_size
        if key == pygame.K_DOWN:
            game_object.centery -= st.GameSettings().tile_size
    else:
        if key == pygame.K_RIGHT:
            game_object.rect.centerx -= st.GameSettings().tile_size
        if key == pygame.K_LEFT:
            game_object.rect.centerx += st.GameSettings().tile_size
        if key == pygame.K_UP:
            game_object.rect.centery += st.GameSettings().tile_size
        if key == pygame.K_DOWN:
            game_object.rect.centery -= st.GameSettings().tile_size

def move_all(key, dungeon, chara):
    """moves all gameobjects movalbe (in dungeon.movables)"""
    """If theres no collision"""
    chara.mov_key_pressed = True
    if check_collission_future(key, dungeon, chara.rect):
        pass
    else:
        for game_object in dungeon.movables:
            move_any(key, game_object)

def abs_distance(rect1, rect2):
    return (abs(rect1.centerx-rect2.centerx) +
                abs(rect1.centery-rect2.centery))

def predict_next_rect(key, rect):
    """Predicts the next square given a direction as a key"""
    newleft = rect.left
    newtop = rect.top
    tilesize = st.GameSettings().tile_size
    
    if key == pygame.K_RIGHT:
        newleft += tilesize
    if key == pygame.K_LEFT:
        newleft -= tilesize
    if key == pygame.K_UP:
        newtop -= tilesize
    if key == pygame.K_DOWN:
        newtop += tilesize

    newrect = pygame.Rect(newleft, newtop, tilesize, tilesize)

    return newrect

def check_collission_future(key, dungeon, rect):
        """Checks collission given a direction"""
        collisionables = (dungeon.enemies_positions + [dungeon.chara.rect] +
                          dungeon.corpses_positions
                          )
        nextrect = predict_next_rect(key, rect)

        if (nextrect in dungeon.tiles and
            nextrect not in collisionables
            ):
            return False
        else:
            return True

def check_keydown_events(event, dungeon, chara):
    """Respond to keypresses."""

    # First checks if the key is active or meta
    # Active keys are the ones that let you act
    # Meta are the ones that control inventory, etc
    if (event.key in st.GameSettings().act_keys 
        and chara.locked == False):
        check_active_events(event, dungeon, chara)
        check_outside_events(dungeon, chara)
        check_passive_events(dungeon, chara)
    elif event.key in st.GameSettings().mov_keys:
        chara.direction = event.key
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
        

def check_active_events(event, dungeon, chara):
    if event.key in st.GameSettings().mov_keys:
        chara.direction = event.key
        move_all(chara.direction, dungeon, chara)
    elif event.key == pygame.K_k:
        chara.use_item(dungeon)
    elif event.key == pygame.K_a:
        chara.attack(dungeon)
        

def check_keyup_events(event, dungeon, chara):
    if event.key == pygame.K_y:
        chara.locked = False
    elif event.key == pygame.K_r:
        chara.running = False
    elif event.key in st.GameSettings().mov_keys:
        chara.mov_key_pressed = False
    elif event.key == pygame.K_a:
        chara.a_pressed = False

def check_keydown_events_running(dungeon, chara):
    if chara.in_danger(dungeon) == False and chara.mov_key_pressed == True:
        move_all(chara.direction, dungeon, chara)
        check_outside_events(dungeon, chara)
        check_passive_events(dungeon, chara)
    elif chara.in_danger(dungeon) == False and chara.a_pressed == True:
        check_outside_events(dungeon, chara)
        check_passive_events(dungeon, chara)
    

def check_events(dungeon, chara):
    """Respond to keypresses and mouse events"""

    if ((chara.running and chara.mov_key_pressed) or 
        (chara.running and chara.a_pressed)):
        check_keydown_events_running(dungeon, chara)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, dungeon, chara)
        elif event.type == pygame.KEYDOWN and chara.inventory_open:
            check_keydown_events_inventory(event, dungeon, chara)
        elif event.type == pygame.KEYDOWN and chara.running == False:
            check_keydown_events(event, dungeon, chara)
        elif event.type == pygame.KEYDOWN and chara.running == True:
                if event.key in st.GameSettings().mov_keys:
                    chara.direction = event.key
                    move_all(chara.direction, dungeon, chara)
                    check_outside_events(dungeon, chara)
                    check_passive_events(dungeon, chara)
                    chara.mov_key_pressed = True
                if event.key == pygame.K_a:
                    chara.attack(dungeon)
                    check_outside_events(dungeon, chara)
                    check_passive_events(dungeon, chara)
                    chara.a_pressed = True

def check_events_menu():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            return True

def check_passive_events(dungeon, chara):

    chara.hp += chara.hp_regen
    chara.san -= chara.san_anti_regen

    if chara.hp > chara.max_hp:
        chara.hp = chara.max_hp

    if chara.san > chara.max_san:
        chara.san = chara.max_san

    if chara.rect in dungeon.item_positions:
        item = dungeon.rect_to_item(chara.rect)
        chara.inventory.append(item)
        dungeon.remove_item(item)

    if chara.rect == dungeon.stairs.position:
        dungeon.reset_dungeon(chara)
        chara.floor += 1
    

def check_outside_events(dungeon, chara):
    for enemy in dungeon.enemies:
        if enemy.hp <= 0:
            dungeon.remove_enemy(enemy)
    for enemy in dungeon.enemies:
        enemy.act(dungeon, chara)


def invert_direction(key):
    if key == pygame.K_DOWN:
        return pygame.K_UP
    elif key == pygame.K_UP:
        return pygame.K_DOWN
    elif key == pygame.K_RIGHT:
        return pygame.K_LEFT
    elif key == pygame.K_LEFT:
        return pygame.K_RIGHT

def check_gameover(chara):
    if chara.hp <= 0 or chara.san <= 0:
        st.SFX().chara_death.play()
        print("game over!")
        return True
    else:
        return False


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