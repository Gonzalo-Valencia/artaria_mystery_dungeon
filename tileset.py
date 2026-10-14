import pygame
import numpy as np

import settings

class Tileset():

    def __init__(self, path):

        # Window where the game is drawn

        # Tileset path
        self.path = path


        # Tileset image and rectangles
        self.image = pygame.image.load(self.path)
        self.rect = self.image.get_rect()

        # Where each tile will be saved for later use
        self.tiles = []

        # Tile properties
        self.length = settings.GameSettings().tile_size

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

class Long_Tileset():

    def __init__(self, path):

        # Window where the game is drawn

        # Tileset path
        self.path = path


        # Tileset image and rectangles
        self.image = pygame.image.load(self.path).convert_alpha()
        self.rect = self.image.get_rect()

        # Where each tile will be saved for later use
        self.tiles = []

        # Tile properties
        self.length = settings.GameSettings().tile_size

        # Where each tile will be saved for later use
        self.tiles = []
        self.load()

    def load(self):
        """Loads all the tiles in a list of rectangles"""
        # The rectangles represent the tiles inside the image
        # from left to right, then from up to down
        # we load each individual tile
        for y in range(0, self.rect.height, self.length*2):
            for x in range(0, self.rect.width, self.length):
                #Rectangle defining each tile
                tile = (x, y, self.length, (self.length)*2)
                tile = pygame.Rect(tile)
                self.tiles.append(tile)

