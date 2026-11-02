import pygame
import settings as st
import game_functions as gf
import random
import render_screen as rs

class Stairs():

    def __init__(self, screen):

        self.screen = screen

        self.image = pygame.image.load(st.SpritePaths().stairs_path)

        self.position = pygame.Rect(0,0,0,0)

    def blitme(self):
        """Draw the character at its current location."""
        self.screen.blit(self.image, self.position)

class ItemChart_alt():

    def __init__(self):
        self.floor1 = ["Blackfire",
                       "Whitefire",
                       "A flower",
                       "Incinerate",
                       "Soul Bind",
                       "Reality Bend",
                       "Living Rot"
                       ]

class ItemChart():

    def __init__(self):
        self.floor1 = [#Item("Blackfire"),
                       #Item("Whitefire"),
                       #Item("A flower"),
                       #Item("Incinerate"),
                       #Item("Soul Bind"),
                       #Item("Reality Bend"),
                       #Item("Living Rot"),

                       Weapon("Boring Sword", 10)
                       ]

class Item():

    def __init__(self, name = ""):
        self.name = name
        self.position = pygame.Rect(0,0,0,0)
        self.image = pygame.image.load(st.SpritePaths().item_path)

    def items_use(self, chara, dungeon):

        chara.inventory.remove(chara.cursor_position-1)   
        
        if self.name == "Blackfire":
            enemy = chara.enemy_infront(dungeon)
            if enemy != None:
                enemy.hp -= st.ItemSettings().blackfire_dmg
            else:
                st.SFX().item_fail.play()
        elif self.name == "Whitefire":
            st.SFX().whitefire.play()
            chara.hp += st.ItemSettings().whitefire_heal
        elif self.name == "A flower":
            st.SFX().a_flower.play()
            chara.san += st.ItemSettings().flower_san_heal
        elif self.name == "Incinerate":
            incineration_tiles = gf.get_squares_in_front(chara.direction, dungeon, chara.position)
            fire_image = pygame.image.load(st.SpritePaths().fire_path)
            for tile in incineration_tiles:
                #dungeon.anim_list.append(rs.Animation(fire_image, tile, 30))
                #dungeon.load_anims(rs.Animation(fire_image, tile), 30)
                dungeon.load_anims(fire_image, tile, 30, "incinerate")

                corpse = dungeon.rect_to_corpse(tile)
                item = dungeon.rect_to_item(tile)
                enemy = dungeon.rect_to_enemy(tile)
                dungeon.screen.blit(fire_image, tile)
                if corpse != None:
                    dungeon.remove_corpse(corpse)
                elif item != None:
                    dungeon.remove_item(item)
                elif enemy != None:
                    dungeon.events.append(enemy.name + " received "
                                          + str(st.ItemSettings().incinerate_dmg) +
                                          " damage!")
                    enemy.hp -= st.ItemSettings().incinerate_dmg
        elif self.name == "Soul Bind":
            enemy = chara.enemy_infront(dungeon)
            if enemy != None:
                st.SFX().soul_bind.play()
                enemy.paralyzed = True
            else:
                st.SFX().item_fail.play()
        elif self.name == "Reality Bend":
            st.SFX().teleport.play
            dungeon.recenter_dg(chara)
        elif self.name == "Living Rot":
            enemy = chara.enemy_infront(dungeon)
            if enemy != None:
                st.SFX().the_rot.play()
                enemy.poisoned = True
            else:
                st.SFX().item_fail.play()

class Weapon(Item):

    def __init__(self, name = "", damage = 0):
        super().__init__(name)
        self.is_equipped = False
        self.is_weapon = True

        self.dmg = damage
        self.slots = 0

    def items_use(self, chara, dungeon):

        dungeon.rerender_text_canvas("Chara equipped the " + self.name + "!")
        if chara.equipped_weapon.name == "Fists":
            chara.equipped_weapon = self
            self.is_equipped = True
        else:
            chara.equipped_weapon.is_equipped == False
            chara.equipped_weapon = self
            self.is_equipped = True


def generate_items_alt(dungeon):
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

def generate_items(dungeon):
    """Returns a list with every item in the dungeon floor"""

    item_ammount = random.choice(st.ItemSettings().item_ammount_chance)
    generated_items = []
    for i in range(item_ammount):
        i_choice = random.choice(ItemChart().floor1)
        i_choice.position = dungeon.choose_position()
        generated_items.append(i_choice)

    return generated_items

def render_items(dungeon, screen):
    image = pygame.image.load(st.SpritePaths().item_path)
    for item in dungeon.items:
        screen.blit(image, item.position)