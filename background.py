import pygame

import settings as st

class Background():

    def __init__(self, screen):
        
        """Initialize the main character and set its starting position."""
        self.screen = screen

        # Load the chara image and get its rect.
        self.image = pygame.image.load(st.SpritePaths().bg_path)
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()

        #Start each new character at the bottom center of the screen
        self.rect.centerx = self.screen_rect.centerx
        self.rect.centery = self.screen_rect.centery

        # Movement flag
        self.moving_right = False
        self.moving_left = False


    def blitme(self):
        """Draw the character at its current location."""
        self.screen.blit(self.image, self.rect)

    def update(self, event):
        if event.key == pygame.K_RIGHT:
            self.rect.centerx -= st.GameSettings().tile_size
        if event.key == pygame.K_LEFT:
            self.rect.centerx += st.GameSettings().tile_size
        if event.key == pygame.K_UP:
            self.rect.centery += st.GameSettings().tile_size
        if event.key == pygame.K_DOWN:
            self.rect.centery -= st.GameSettings().tile_size