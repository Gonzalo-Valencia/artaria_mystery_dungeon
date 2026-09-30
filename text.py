import pygame
import settings as st
import game_functions as gf

def render_text(screen, text:str, rect_tuple:tuple):
    """Renders the text in the corner tuple (x,y)"""
    myfont = st.UISettings().menu_font
    font_color = st.UISettings().font_color

    text_surface = myfont.render(text, 
                                 False, font_color)

    screen.blit(text_surface, rect_tuple)

    
def render_text_box(screen, text:str, rect_tuple:tuple):
    square = pygame.Surface((64*2, 64))
    screen.blit(square, rect_tuple)
    render_text(screen, text, rect_tuple)

