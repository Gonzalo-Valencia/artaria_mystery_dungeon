import pygame
import random
import settings as st
import game_functions as gf


class Enemy():

    def __init__(self):


        # Load the enemy image and get its rect.
        self.image = pygame.image.load(st.SpritePaths().chara_path)
        self.rect = self.image.get_rect()

        self.name = "missingNo"
        self.hp = 0
        self.dmg = 0
        self.id = -1
        self.position = pygame.Rect(0,0,0,0)

        self.aggro = False

    def assign_stats(self, hp, dmg, e_id):
        """assigns stats to a blank enemy"""
        self.hp = hp
        self.dmg = dmg
        self.id = e_id

    def name_to_stats(self, name):

        if name == 'slime':
            self.name = name
            self.assign_stats(1,5,0)
        if name == 'skelet':
            self.name = name
            self.assign_stats(2,10,1)
        if name == 'mage':
            self.name = name
            self.assign_stats(4,15,2)
        if name == 'dragon':
            self.name = name
            self.assign_stats(6,20,3)

    def clash(self, dungeon, chara):
        self.hp -= chara.dmg
        print(self.name +": yeouch!")
        if self.hp <= 0:
            dungeon.remove_enemy(self)
            print(self.name +": DEAD!")
        else:
            chara.hp -= self.dmg
            print("Chara: yeouch!")

    def move(self, dungeon, chara):
        """Tries to move the enemy"""

        if gf.abs_distance(self.position, chara.rect) < 6*st.GameSettings().tile_size:
            #if theyre in aggro, the go to you
            moves = [pygame.K_DOWN, pygame.K_UP, pygame.K_LEFT, pygame.K_RIGHT]
            optimal = False
            while optimal == False and moves:
                #Thell chose at random whatever makes them close
                direction = random.choice(moves)
                moves.remove(direction)
                newrect = gf.predict_next_rect(direction, self.position)
                if (gf.abs_distance(newrect, chara.rect)
                     < gf.abs_distance(self.position, chara.rect) and 
                     gf.check_collission_future(direction, dungeon, self.position) == False
                     ):
                    #If its a legal move and they get close, they move. 
                    # if not, they dont do anything
                    gf.move_any(gf.invert_direction(direction), self.position)
                    optimal = True
        else:
            direction = random.choice([pygame.K_DOWN, pygame.K_UP, pygame.K_LEFT, pygame.K_RIGHT])
            
            if gf.check_collission_future(direction, dungeon, self.position) == False:
                gf.move_any(gf.invert_direction(direction), self.position)

    def aggro(self, dungeon, chara):
        if (abs(chara.rect.centerx-self.position.centerx) < 6 or
            abs(chara.rect.centery-self.position.centery) < 6
            ):
            self.aggro = True

    def attack(self, dungeon, chara):
        st.SFX().chara_attacked.play()
        chara.hp -= self.dmg

        dungeon.events.append( "The " + self.name + " dealt " + 
                              str(self.dmg) + "dmg to Chara!" )


    def act(self, dungeon, chara):
        for key in (pygame.K_LEFT, pygame.K_RIGHT, pygame.K_DOWN, pygame.K_UP):
            newrect = gf.predict_next_rect(key, self.position)
            if chara.rect == newrect:
                break

        if chara.rect == newrect:
            self.attack(dungeon, chara)
        else:
            self.move(dungeon, chara)

class EnemyChart():

    def __init__(self):
        self.floor1 = ['slime', 'skelet', 'mage', 'dragon']

def generate_enemies(dungeon):
    weight = 0
    generated_enemies = []
    while weight < 17:
        name_choice = random.choice(EnemyChart().floor1)
        e_choice = Enemy()
        e_choice.name_to_stats(name_choice)
        e_choice.position = dungeon.choose_position()

        generated_enemies.append(e_choice)

        weight += e_choice.hp

    return generated_enemies

def render_enemies(dungeon, screen):

    for enemy in dungeon.enemies:
        tileset = st.Tilesets().enemy_ts
        cutout = tileset.tiles[enemy.id]


        screen.blit(tileset.image, enemy.position, cutout)


class Corpse():

    def __init__(self, position):

        self.image = pygame.image.load(st.SpritePaths().item_path)
        self.position = position