import sys

import pygame
import settings as st
from tileset import Tileset
import enemies
import text
import game_items

def move_any_alt(event, game_object):
    """Moves the object contrary to the movement of the character"""
    # i.e. moves the background, tiles, etc
    # game_object must have a rect
    if isinstance(game_object, pygame.rect.Rect):
        if event.key == pygame.K_RIGHT:
            game_object.centerx -= st.GameSettings().tile_size
        if event.key == pygame.K_LEFT:
            game_object.centerx += st.GameSettings().tile_size
        if event.key == pygame.K_UP:
            game_object.centery += st.GameSettings().tile_size
        if event.key == pygame.K_DOWN:
            game_object.centery -= st.GameSettings().tile_size
    else:
        if event.key == pygame.K_RIGHT:
            game_object.rect.centerx -= st.GameSettings().tile_size
        if event.key == pygame.K_LEFT:
            game_object.rect.centerx += st.GameSettings().tile_size
        if event.key == pygame.K_UP:
            game_object.rect.centery += st.GameSettings().tile_size
        if event.key == pygame.K_DOWN:
            game_object.rect.centery -= st.GameSettings().tile_size

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
        collisionables = dungeon.enemies_positions + [dungeon.chara.rect]
        nextrect = predict_next_rect(key, rect)

        if (nextrect in dungeon.tiles and
            nextrect not in collisionables
            ):
            return False
        else:
            return True

def move_all(event, dungeon, chara):
    """moves all gameobjects movalbe (in dungeon.movables)"""
    """If theres no collision"""

    if check_collission_future(event.key, dungeon, chara.rect):
        pass
    else:
        for game_object in dungeon.movables:
            move_any(event.key, game_object)

def check_keydown_events(event, dungeon, chara):
    """Respond to keypresses."""
    if event.key in st.GameSettings().mov_keys:
        chara.direction = event.key
        move_all(event, dungeon, chara)
    elif event.key == pygame.K_d:
        dungeon.reset_dungeon(chara)
    elif event.key == pygame.K_r:
        dungeon.recenter_dg(dungeon)
    elif event.key == pygame.K_a:
        chara.attack(dungeon)
    elif event.key == pygame.K_ESCAPE:
        sys.exit()
    elif event.key == pygame.K_i:
        chara.cursor_position -= 1
    elif event.key == pygame.K_m:
        chara.cursor_position += 1
    elif event.key == pygame.K_k:
        chara.use_item(dungeon)

def check_events(dungeon, chara):
    """Respond to keypresses and mouse events"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, dungeon, chara)
            check_outside_events(dungeon, chara)

def check_events_menu():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            return True

def check_passive_events(dungeon, chara):
    if chara.rect in dungeon.item_positions:
        item = dungeon.rect_to_item(chara.rect)
        chara.inventory.append(item)
        dungeon.remove_item(item)

    for enemy in dungeon.enemies:
        if enemy.hp <= 0:
            dungeon.remove_enemy(enemy)

    if chara.rect == dungeon.stairs.position:
        dungeon.reset_dungeon(chara)
        chara.floor += 1
    

def check_outside_events(dungeon, chara):
    for enemy in dungeon.enemies:
        enemy.move(dungeon, chara)

def update_screen(screen, realscreen, i_canvas, chara, tileset, dungeon):
    """Update images on the screen and flip to the new screen."""
    # Redraw the screen during each pass through the loop.

    screen.fill(st.UISettings().bg_color)

    dungeon.render_dungeon(tileset)
    game_items.render_items(dungeon, screen)
    enemies.render_enemies(dungeon, screen)
    dungeon.stairs.blitme()
    chara.blitme()

    text.render_text_box(screen, str(chara.hp), (0,0))
    text.render_text_box(screen, str(chara.floor), (0,64))

    
    # Make the most recently drawn screen visible


    realscreen.fill(st.UISettings().bg_color)

    marginl = st.UISettings().mini_screen_margins_left
    marginu = st.UISettings().mini_screen_margins_up
    realscreen.blit(screen, (marginl,marginu))


    i_canvas.fill(st.UISettings().bg_color)
    chara.render_inventory(i_canvas)
    i_canvas.blit(pygame.image.load(st.SpritePaths().cursor_path),
                    (0,(chara.cursor_position-1)*st.UISettings().text_line_height)
                    )

    realscreen.blit(i_canvas, st.UISettings().inventory_place)

    pygame.display.flip()

def update_screen_main_menu(screen, realscreen):

    lines = ["Game Start", "Settings", "Quit"]
    height_of_line = st.UISettings().text_margin_up

    realscreen.fill(st.UISettings().bg_color)
    for line in lines:
        text.render_text(realscreen, line, 
                        (st.UISettings().text_margin_left,
                        height_of_line,
                        ))
        height_of_line += st.UISettings().text_line_height

    #realscreen.blit(screen, (0,0))
    pygame.display.flip()


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
    if chara.hp <= 0:
        print("game over!")
        return True
    else:
        return False