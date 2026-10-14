import sys
import pygame

import settings as st
from chara import Chara
from background import Background
from tileset import Tileset
from dungeon import Dungeon
from enemies import generate_enemies
import game_functions as gf
import text

def run_game():
    # Make the character:
    pygame.init()
    pygame.joystick.init()

    joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]
    print(joysticks)

    pygame.display.set_caption("Artaria Mystery Dungeon")
    screen = pygame.display.set_mode(
            (st.UISettings().screen_width *0.25, st.UISettings().screen_height * 0.25),
            vsync=1
            )
    chara = Chara(screen)
    running = False
    # Start the main loop for the game.
    while True:
        # Watch for keyboard and mouse events.
        for event in pygame.event.get():
            print(event)
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.JOYBUTTONDOWN:
                print(event)
            elif event.type == pygame.JOYHATMOTION:
                if event.value[0] == -1:
                    print("EY YOW HAT LEFT")
        chara.blitme()

        pygame.display.flip()


#run_game()


# Define separate attack behaviors
def normal_attack():
  return "Basic strike."


def aggressive_attack():
  return "Raging combo attack!"


class Enemy:

  def __init__(self, name, attack_behavior=normal_attack):
    self.name = name
    self.attack_behavior = attack_behavior  # Assigning a function as an attribute

  def attack(self):
    return self.attack_behavior()


# --- Example Usage ---
# Create a normal enemy and an aggressive enemy using the same class
goblin = Enemy("Goblin")
orc = Enemy("Orc", aggressive_attack)

print(f"{goblin.name}: {goblin.attack()}")  # Output: Goblin: Basic strike.
print(f"{orc.name}: {orc.attack()}")  # Output: Orc: Raging combo attack!

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

                def move(self, dungeon, chara):
        """Tries to move the enemy"""

        if gf.abs_distance(self.position, chara.rect) < 6*st.GameSettings().tile_size:
            #if theyre in aggro, the go to you
            moves = [(0,1), (0,-1), (1,0), (-1,0), (1,1), (-1,1), (1,-1), (-1,-1)]
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
            direction = random.choice([(0,1), (0,-1), (1,0), (-1,0), (1,1), (-1,1), (1,-1), (-1,-1)])
            
            if gf.check_collission_future(direction, dungeon, self.position) == False:
                gf.move_any(gf.invert_direction(direction), self.position)

    def attack(self, dungeon, chara):
        st.SFX().chara_attacked.play()
        chara.hp -= self.dmg

        dungeon.events.append( "The " + self.name + " dealt " + 
                              str(self.dmg) + "dmg to Chara!" )

    def act_alt(self, dungeon, chara):
        """First it gets the chara rect in the vicinity"""
        for direction in [(0,1), (0,-1), (1,0), (-1,0), (1,1), (-1,1), (1,-1), (-1,-1)]:
            newrect = gf.predict_next_rect(direction, self.position)
            if chara.rect == newrect:
                break

        if chara.rect == newrect:
            self.attack(dungeon, chara)
        else:
            # If it doesnt find chara, then
            self.move(dungeon, chara)
