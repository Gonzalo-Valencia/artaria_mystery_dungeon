import pygame
import game_functions as gf
import settings as st
import text
import game_items
import enemies




def update_screen(realscreen, canvas, game_canvas, i_canvas, text_canvas,
                   chara, tileset, dungeon):
    """Update images on the screen and flip to the new screen."""
    # Redraw the screen during each pass through the loop.

    # ---------------- Game Canvas  -------------------:
    game_canvas.fill(st.UISettings().bg_color)

    dungeon.render_dungeon(tileset)
    game_items.render_items(dungeon, game_canvas)
    dungeon.stairs.blitme()
    dungeon.render_corpses()
    enemies.render_enemies(dungeon, game_canvas)
    chara.blitme()

    text.render_text_box(game_canvas, str(chara.hp), (0,0))
    text.render_text_box(game_canvas, str(chara.floor), (0,96))
    text.render_text_box(game_canvas, str(chara.flesh), (0,64))
    text.render_text_box(game_canvas, str(chara.san), (0,32))

    # ----------------- Inventory Canvas  -------------------:
    i_canvas.fill(st.UISettings().bg_color)
    update_inventory(i_canvas, chara, dungeon)
    # ----------------- Text canvas  -------------------:
    text_canvas.fill(st.UISettings().bg_color)

    update_text_canvas(text_canvas, dungeon, chara)



    # ----------------- Canvas  -------------------:
    realscreen.fill(st.UISettings().bg_color)

    marginl = st.UISettings().mini_screen_margins_left
    marginu = st.UISettings().mini_screen_margins_up

    # We render the dungeon
    canvas.blit(game_canvas, (marginl,marginu))
    # We render the inventory
    canvas.blit(i_canvas, st.UISettings().inventory_place)

    canvas.blit(text_canvas, st.UISettings().text_canvas_place)

    # We render the ui
    update_ui_overlay(canvas, chara)


    # ----------------- Real Screen  -------------------:
    realscreen.blit(canvas, (0,0))

    pygame.display.flip()

def update_screen_main_menu(realscreen, canvas, game_canvas, i_canvas):

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

def update_ui_overlay(canvas, chara):
    canvas.blit(chara.ui_overlay, (0,0))

def update_inventory(i_canvas, chara, dungeon):
    if chara.inventory_page == 0:
        text.render_text(i_canvas, "CONTROLS",
                         (st.GameSettings().tile_size,0))
        render_controls_page(i_canvas)
    else:
        text.render_text(i_canvas, "INVENTORY", (st.GameSettings().tile_size,0))

        render_inventory_page(i_canvas, chara)

        # Render the cursor
        i_canvas.blit(pygame.image.load(st.SpritePaths().cursor_path),
                        (0,(chara.cursor_position)*st.UISettings().text_line_height)
                        )

def render_controls_page(i_canvas):
    """Renders all the control explanations"""
    controls = ["A: Attack", "Dir: Move",
                "X: Inventory/Examine", "Y: Lock in place",
                "B+Dir: Run", "B+A: Fast forward",
                "R: Lock Diagonal"]
    for i in range(len(controls)):
        text.render_text(i_canvas, controls[i],
                            (st.GameSettings().tile_size,
                            (i+1)*st.UISettings().text_line_height
                            ))


def render_inventory_page(i_canvas, chara):
    inventory_page = chara.inventory[(chara.inventory_page-1)*7:(chara.inventory_page)*7]

    for i in range(len(inventory_page)):
            text.render_text(i_canvas, chara.inventory[i].name,
                                (st.GameSettings().tile_size,
                                (i+1)*st.UISettings().text_line_height
                                ))

    text.render_text(i_canvas, "<" + str(chara.inventory_page) + "/" + str(chara.max_pages) + ">",
                      (2*st.GameSettings().tile_size, 8*st.GameSettings().tile_size))


def update_text_canvas(text_canvas, dungeon, chara):

    if dungeon.events:
        for i in range(1, len(dungeon.events)+1):
            text.render_text(text_canvas, dungeon.events[-i],
                            (0, i*st.GameSettings().tile_size)
                            )
