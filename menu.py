import pygame
import settings as st


class Menu():

    def __init__(self):

        self.lines = []
        self.canvas = pygame.Surface(st.UISettings().screen_size, pygame.SRCALPHA)
        self.background = pygame.image.load(st.SpritePaths().main_menu_path)

        self.canvas.blit(self.background, (0,0))
        
        self.cursor_pos = 0
        self.run_game = False


