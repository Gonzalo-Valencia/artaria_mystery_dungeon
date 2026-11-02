import pygame
import random
import settings as st
import game_functions as gf



def move(enemy, dungeon, chara):
        """Tries to move the enemy"""
        if enemy.paralyzed == False:
            if gf.abs_distance(enemy.position, chara.position) < 6*st.GameSettings().tile_size:
                #if theyre in aggro, the go to you
                moves = [(0,1), (0,-1), (1,0), (-1,0), (1,1), (-1,1), (1,-1), (-1,-1)]
                optimal = False
                while optimal == False and moves:
                    #Thell chose at random whatever makes them close
                    direction = random.choice(moves)
                    moves.remove(direction)
                    newrect = gf.predict_next_rect(direction, enemy.position)
                    if (gf.abs_distance(newrect, chara.position)
                        < gf.abs_distance(enemy.position, chara.position) and 
                        gf.check_collission_future(direction, dungeon, enemy.position) == False
                        ):
                        #If its a legal move and they get close, they move. 
                        # if not, they dont do anything
                        gf.create_any_move_anim(direction, enemy, dungeon, "enemy")
                        gf.move_any(gf.invert_direction(direction), enemy.position, dungeon)
            
                        optimal = True
            else:
                direction = random.choice([(0,1), (0,-1), (1,0), (-1,0), (1,1), (-1,1), (1,-1), (-1,-1)])
                
                if gf.check_collission_future(direction, dungeon, enemy.position) == False:
                    gf.create_any_move_anim(direction, enemy, dungeon, "enemy")
                    gf.move_any(gf.invert_direction(direction), enemy.position, dungeon)

def flee(enemy, dungeon, chara):
        if enemy.paralyzed == False:
            if gf.abs_distance(enemy.position, chara.position) < 6*st.GameSettings().tile_size:
                #if theyre in aggro, the go to you
                moves = [(0,1), (0,-1), (1,0), (-1,0), (1,1), (-1,1), (1,-1), (-1,-1)]
                optimal = False
                while optimal == False and moves:
                    #Thell chose at random whatever makes them close
                    direction = random.choice(moves)
                    moves.remove(direction)
                    newrect = gf.predict_next_rect(direction, enemy.position)
                    if (gf.abs_distance(newrect, chara.position)
                        > gf.abs_distance(enemy.position, chara.position) and 
                        gf.check_collission_future(direction, dungeon, enemy.position) == False
                        ):
                        #If its a legal move and they get close, they move. 
                        # if not, they dont do anything
                        gf.create_any_move_anim(direction, enemy, dungeon, "enemy")
                        gf.move_any(gf.invert_direction(direction), enemy.position, dungeon)
                        optimal = True
            else:
                direction = random.choice([(0,1), (0,-1), (1,0), (-1,0), (1,1), (-1,1), (1,-1), (-1,-1)])
                
                if gf.check_collission_future(direction, dungeon, enemy.position) == False:
                    gf.create_any_move_anim(direction, enemy, dungeon, "enemy")
                    gf.move_any(gf.invert_direction(direction), enemy.position, dungeon)

def attack(enemy, dungeon, chara):
    st.SFX().chara_attacked.play()
    chara.hp -= enemy.dmg

    message = ("The " + enemy.name + " dealt " + 
                        str(enemy.dmg) + "dmg to Chara!")
    dungeon.rerender_text_canvas(message)
    #dungeon.events.append( "The " + enemy.name + " dealt " + 
    #                    str(enemy.dmg) + "dmg to Chara!" )

def normal_behaviour(enemy, dungeon, chara):
    for direction in [(0,1), (0,-1), (1,0), (-1,0), (1,1), (-1,1), (1,-1), (-1,-1)]:
        newrect = gf.predict_next_rect(direction, enemy.position)
        newdirection = direction
        if chara.position == newrect:
            break

    if chara.position == newrect:
        if newdirection in [(1,1), (-1,1), (1,-1), (-1,-1)]:
            if (gf.predict_next_rect((newdirection[0], 0), enemy.position) in dungeon.tiles and
                gf.predict_next_rect((0, newdirection[1]), enemy.position) in dungeon.tiles):
                attack(enemy, dungeon, chara)
            else:
                move(enemy, dungeon, chara)
        else:
            attack(enemy, dungeon, chara)
    else:
        # If it doesnt find chara, then
        move(enemy, dungeon, chara)

def corpse_eater_behaviour(enemy, dungeon, chara):

    closest_corpse_pos = gf.find_closest(enemy.position, *dungeon.corpses_positions)
    if closest_corpse_pos != enemy.position:
        closest_corpse = dungeon.rect_to_corpse(closest_corpse_pos)

    
    

    if enemy.hp < enemy.max_hp*0.5:
        # If its life is low, it finds a corpse and goes to consume it
        pass

def coward_behaviour(enemy, dungeon, chara):
    # If its life is low, it will flee
    if enemy.hp < enemy.max_hp*0.5:
        flee(enemy, dungeon, chara)
    else:
        for direction in [(0,1), (0,-1), (1,0), (-1,0), (1,1), (-1,1), (1,-1), (-1,-1)]:
            newrect = gf.predict_next_rect(direction, enemy.position)
            newdirection = direction
            if chara.position == newrect:
                break
        if chara.position == newrect:
            if newdirection in [(1,1), (-1,1), (1,-1), (-1,-1)]:
                if (gf.predict_next_rect((newdirection[0], 0), enemy.position) in dungeon.tiles and
                    gf.predict_next_rect((0, newdirection[1]), enemy.position) in dungeon.tiles):
                    attack(enemy, dungeon, chara)
                else:
                    move(enemy, dungeon, chara)
            else:
                attack(enemy, dungeon, chara)
        else:
            # If it doesnt find chara, then
            move(enemy, dungeon, chara)


class Enemy():

    def __init__(self, name = "missingNo", hp = 0, dmg = 0, e_id = -1,
                 behaviour = normal_behaviour, position = pygame.Rect(0,0,0,0),
                 ):

        self.name = name
        self.hp = hp
        self.max_hp = hp
        self.dmg = dmg
        self.id = e_id 
        self.position = position

        self.images = pygame.Surface((st.GameSettings().tile_size, st.GameSettings().tile_size*4), pygame.SRCALPHA)
        self.images.blit(st.Tilesets().enemy_ts.image, 
                                (0,0), 
                                st.Tilesets().enemy_ts.tiles[self.id])
        self.images.blit(st.Tilesets().enemy_ts.image, 
                        (0,st.GameSettings().tile_size), 
                        st.Tilesets().enemy_ts.tiles[self.id+8])

        self.image = pygame.Surface((st.GameSettings().tile_size, st.GameSettings().tile_size), pygame.SRCALPHA)
        self.image.blit(st.Tilesets().enemy_ts.image, 
                                (0,0), 
                                st.Tilesets().enemy_ts.tiles[self.id])
        # Statuses ------------
        # Unable to move
        self.paralyzed = False
        self.poisoned = False

        self.act = lambda dungeon, chara: behaviour(self, dungeon, chara)

        #From 1 to 60
        self.anim_loop = 0


class EnemyChart():

    def __init__(self):
        self.floor1 = ['slime', 'skelet', 'mage', 'dragon']

class Bestiary():

    def __init__(self):
        self.slime = Enemy('slime', 10, 5, 0)
        self.skelet = Enemy('skelet', 20, 10, 1)
        self.mage = Enemy('mage', 60, 15, 2, behaviour=coward_behaviour)
        self.dragon = Enemy('dragon', 80, 20, 3)

        self.floor1 = [self.slime, self.skelet, self.mage, self.dragon]

def name_to_stats(name):
    if name == 'slime':
        return Enemy(name, 1,5,0)
    if name == 'skelet':
        return Enemy(name, 2,10,1)
    if name == 'mage':
        return Enemy(name, 4,15,2)
    if name == 'dragon':
        return Enemy(name, 6,20,3)


def generate_enemies(dungeon):
    weight = 0
    generated_enemies = []
    while weight < 16:
        #name_choice = random.choice(EnemyChart().floor1)
        #e_choice = name_to_stats(name_choice)
        e_choice = random.choice(Bestiary().floor1)
        e_choice.position = dungeon.choose_position()

        generated_enemies.append(e_choice)

        weight += e_choice.hp

    return generated_enemies

def render_enemies(dungeon, screen):

    for enemy in dungeon.enemies:
        
        if enemy.anim_loop> 60:
            enemy.anim_loop = 1
        else:
            enemy.anim_loop +=1

        if enemy.anim_loop <= 30:
            #cutout = st.Tilesets().enemy_ts.tiles[enemy.id+8]
            screen.blit(enemy.image, enemy.position, (0,st.GameSettings().tile_size))
        else:
            #cutout = st.Tilesets().enemy_ts.tiles[enemy.id]
            screen.blit(enemy.image, enemy.position, (0,st.GameSettings().tile_size))


        #screen.blit(st.Tilesets().enemy_ts.image, enemy.position, cutout)

class Corpse():

    def __init__(self, position):

        self.images = pygame.image.load(st.SpritePaths().item_path)
        self.position = position