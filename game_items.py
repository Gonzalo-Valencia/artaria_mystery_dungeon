import pygame
import settings as st
import game_functions as gf
import random

class Stairs():

    def __init__(self, screen):

        self.screen = screen

        self.image = pygame.image.load(st.SpritePaths().stairs_path)

        self.position = pygame.Rect(0,0,0,0)

    def blitme(self):
        """Draw the character at its current location."""
        self.screen.blit(self.image, self.position)


class Weapon():

    def __init__(self):

        self.is_equipped = False

        self.dmg = 0
        self.slots = 0

class ItemChart():

    def __init__(self):
        self.floor1 = ["Blackfire",
                       "Whitefire",
                       "A flower"
                       #"Incinerate",
                       #"Soul Bind",
                       #"Reality Bend",
                       #"Blaze of Madness"
                       ]

class Item():

    def __init__(self):
        self.name = ""
        self.position = pygame.Rect(0,0,0,0)

    def items_use(self, chara, dungeon):

        if self.name == "Blackfire":
            enemy = chara.enemy_infront(dungeon)
            if enemy != None:
                print(enemy.name)
                print(str(enemy.hp))
                enemy.hp -= st.ItemSettings().blackfire_dmg
                print(str(enemy.hp))
        elif self.name == "Whitefire":
            chara.hp += st.ItemSettings().whitefire_heal
        elif self.name == "A flower":
            chara.san += st.ItemSettings().flower_san_heal



def generate_items(dungeon):
    """Returns a list with every item in the dungeon floor"""

    item_ammount = random.choice(st.ItemSettings().item_ammount_chance)
    generated_items = []
    for i in range(item_ammount):
        name_choice = random.choice(ItemChart().floor1)
        i_choice = Item()
        i_choice.name = name_choice
        i_choice.position = dungeon.choose_position()
        generated_items.append(i_choice)

    return generated_items

def render_items(dungeon, screen):
    image = pygame.image.load(st.SpritePaths().item_path)
    for item in dungeon.items:
        screen.blit(image, item.position)