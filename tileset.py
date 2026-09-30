import pygame
import numpy as np

import settings

class Tileset():

    def __init__(self, screen):

        # Window where the game is drawn
        self.screen = screen

        # Tileset path
        self.path = settings.SpritePaths().tileset_path


        # Tileset image and rectangles
        self.image = pygame.image.load(self.path)
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()

        # Where each tile will be saved for later use
        self.tiles = []

        # Tile properties
        self.length = settings.GameSettings().tile_size
        self.size = ( self.length , self.length )
        self.rect.centerx = self.screen_rect.centerx
        self.rect.centery = self.screen_rect.centery

        # Where each tile will be saved for later use
        self.tiles = []
        self.load()

    def load(self):
        """Loads all the tiles in a list of rectangles"""
        # The rectangles represent the tiles inside the image
        # from left to right, then from up to down
        # we load each individual tile
        for y in range(0, self.rect.height, self.length):
            for x in range(0, self.rect.width, self.length):
                #Rectangle defining each tile
                tile = (x, y, self.length, self.length)
                tile = pygame.Rect(tile)
                self.tiles.append(tile)

    def render(self):
        """Renders the whole image, tile by tile"""
        # from left to right

        self.rect = self.tiles[0]
        self.rect.centerx = self.screen_rect.centerx
        self.rect.centery = self.screen_rect.centery

        for tile in self.tiles:
            
            self.screen.blit(self.image, self.rect , tile)  
            self.rect.centerx += self.length

    def render_alt(self):
        """Renders the whole image, tile by tile"""
        # from left to right, then from up to down
        # we load each individual tile
        for y in range(0, self.rect.height, self.length):
            
            for x in range(0, self.rect.width, self.length):
                self.screen.blit(self.image, self.rect , (x, y, self.length, self.length))
                self.rect.centerx += self.length
            self.rect.centery += self.length
            # Reset the position of the camera rendering
            self.rect.centerx = self.screen_rect.centerx
        self.rect.centery = self.screen_rect.centery