import random
import pygame

import game_functions as gf
import settings as st
import enemies
import game_items

class Dungeon():

    def __init__(self, screen, chara):

        self.screen = screen
        self.chara = chara

        self.tilesize = st.GameSettings().tile_size
        
        self.dimensions = st.GameSettings().dungeon_dim
        #self.x_division = random.randint(2,8)
        #self.y_division = random.randint(2,4)
        self.x_division = 3
        self.y_division = 3     
        self.room_prob = 0.66

        self.x_room_width_division = int(self.dimensions[0]/self.x_division)
        self.y_room_height_division = int(self.dimensions[1]/self.y_division)

        self.x_room_max = self.x_room_width_division -1
        self.y_room_max = self.y_room_height_division -1

        # Collection of the rooms as rects
        self.rooms = []
        # generates all the rooms
        self.generate()

        # All the walkable tiles in the dungeon
        self.tiles = []
        # joins all the rooms
        self.join_all_rooms()
        # puts all the room tiles into the self.tiles
        self.room_to_tiles()

        # All edge non-walkable tiles
        # Ex: { (-1,1) : all left upper corners, (-1,0) : all left walls, ....}
        self.edges = {}
        self.edges[-1] = []
        for i in range(25):
            self.edges[i] = []
        self.get_edges()

        self.edges_list=[]
        self.edges_to_list()

        # List of enemies
        self.enemies = enemies.generate_enemies(self)
        # Linked list of rectangles where the enmies are
        self.enemies_positions = []
        self.enemies_positions_to_list()

        self.items = game_items.generate_items(self)
        self.item_positions = []
        self.item_positions_to_list()

        self.stairs = game_items.Stairs(screen)
        self.stairs.position = self.choose_position()

        self.movables = (self.tiles + self.edges_list +
                         self.enemies_positions + self.item_positions +
                         [self.stairs.position]
                         )
        #self.graph = {}

        # List of strings explaining what happened lately
        self.events = []

        # List of corpses in the dungeon
        self.corpses = []
        self.corpses_positions = []
        

    def choose_position(self):
        """Returns a random walkable tile inside the dungeon"""
        tilesize = st.GameSettings().tile_size

        room = random.choice(self.rooms)
        left = random.randrange(room.left, room.left+room.width-tilesize, tilesize)
        top = random.randrange(room.top, room.top+room.height-tilesize, tilesize)

        return pygame.Rect(left, top, tilesize, tilesize)

    def enemies_positions_to_list(self):
        """Saves every enemy position in a linked list"""
        # Modifying this list later on will modify the enemies positions
        self.enemies_positions = []
        for enemy in self.enemies:
            self.enemies_positions.append(enemy.position)

    def item_positions_to_list(self):


        self.item_positions = []
        for item in self.items:
            self.item_positions.append(item.position)

    def generate(self):

        while len(self.rooms) == 0 or len (self.rooms)> 10:
            self.rooms = []

            for j in range(0, self.dimensions[1], self.y_room_height_division):
                for i in range(0, self.dimensions[0], self.x_room_width_division):
                    if random.random() <= self.room_prob:    
                        # Room has the two coordinates of the rectangle
                        room_ratio_flag = 0
                        while room_ratio_flag>=2 or room_ratio_flag<=0.5:
                            x_room_dim = random.randint(5, self.x_room_max)
                            y_room_dim = random.randint(5, self.y_room_max)
                            room_ratio_flag = x_room_dim/y_room_dim

                        left = j * st.GameSettings().tile_size
                        top = i * st.GameSettings().tile_size
                        width = x_room_dim * st.GameSettings().tile_size
                        heigth = y_room_dim * st.GameSettings().tile_size

                        room = pygame.Rect((left, top, width, heigth))
                        self.rooms.append(room)

    def rect_to_tiles(self):
        """Returns a list of tuples"""
        """Each tuple is the room in tiles instead of pixels"""

        dungeon_rooms_in_tiles = []
        for room in self.rooms:
            falseroom = []
            for i in room:
                falsei = i/64
                falseroom.append(falsei)
            dungeon_rooms_in_tiles.append((
                falseroom[0],
                falseroom[1],
                falseroom[2],
                falseroom[3]))
            
        return dungeon_rooms_in_tiles

    def room_to_tiles(self):
        """Appends all the tiles of the rooms into the self.tiles"""
        tilesize = st.GameSettings().tile_size
        for room in self.rooms:
            for i in range(room.left, room.left+room.width, tilesize):
                for j in range(room.top, room.top+room.height, tilesize):
                    rectangle = pygame.Rect(i, j, tilesize, tilesize)
                    self.tiles.append(rectangle)

    def join_rooms_h(self, room1, room2):
        """Given two rooms, joins them with paths horizontally"""   
        """ROOM 1 MUST BE TO THE LEFT OF ROOM 2"""

        tilesize = st.GameSettings().tile_size
        h1 = room1.height
        h2 = room2.height
        top1 = room1.top
        top2 = room2.top
        w1 = room1.width
        w2 = room2.width
        left1 = room1.left
        left2 = room2.left

        if left2 < left1:
            raise ValueError("Room2 to the right of room1!")
        else:

            #This is just the top of the tile where the path starts
            tile1 = random.randrange(top1, top1+h1, tilesize)
            tile2 = random.randrange(top2, top2+h2, tilesize)
            
            if tile1 == tile2:
                #If the path is a line, add the line to the tiles
                for i in range(left1+w1, left2, tilesize):
                        rectangle = pygame.Rect(i, tile1, tilesize, tilesize)
                        self.tiles.append(rectangle)
            else:
                # if not, choose a random point in the middle and
                # make the path three segments
                tile3 = random.randrange(left1+w1, left2, tilesize)

                for i in range(left1+w1, tile3, tilesize):
                    rectangle = pygame.Rect(i, tile1, tilesize, tilesize)
                    self.tiles.append(rectangle)
                if tile1 < tile2:
                    for i in range(tile1, tile2, tilesize):
                        rectangle = pygame.Rect(tile3, i, tilesize, tilesize)
                        self.tiles.append(rectangle)
                elif tile2 < tile1:
                    for i in range(tile2, tile1, tilesize):
                        rectangle = pygame.Rect(tile3-tilesize, i, tilesize, tilesize)
                        self.tiles.append(rectangle)
                for i in range(tile3, left2, tilesize):
                    rectangle = pygame.Rect(i, tile2, tilesize, tilesize)
                    self.tiles.append(rectangle)

    def join_rooms_v(self, room1, room2):
        """Given two rooms, joins them with paths vertically"""   
        """ROOM 1 MUST BE UP FROM OF ROOM 2"""

        tilesize = st.GameSettings().tile_size
        h1 = room1.height
        h2 = room2.height
        top1 = room1.top
        top2 = room2.top
        w1 = room1.width
        w2 = room2.width
        left1 = room1.left
        left2 = room2.left

        if top2 < top1:
            raise ValueError("Room2 to up of room1!")
        else:

            #This is just the left of the tile where the path starts
            tile1 = random.randrange(left1, left1+w1, tilesize)
            tile2 = random.randrange(left2, left2+w2, tilesize)
            
            if tile1 == tile2:
                #If the path is a line, add the line to the tiles
                for i in range(top1+h1, top2, tilesize):
                        rectangle = pygame.Rect(tile1, i, tilesize, tilesize)
                        self.tiles.append(rectangle)
            else:
                # First case: tile1 < tile2

                # if not, choose a random point in the middle and
                # make the path three segments
                
                tile3 = random.randrange(top1+h1, top2, tilesize)

                for i in range(top1+h1, tile3, tilesize):
                    rectangle = pygame.Rect(tile1, i, tilesize, tilesize)
                    self.tiles.append(rectangle)
                if tile1 < tile2:
                    for i in range(tile1, tile2, tilesize):
                        rectangle = pygame.Rect(i, tile3, tilesize, tilesize)
                        self.tiles.append(rectangle)
                elif tile2 < tile1:
                    for i in range(tile2, tile1, tilesize):
                        rectangle = pygame.Rect(i, tile3-tilesize, tilesize, tilesize)
                        self.tiles.append(rectangle)
                for i in range(tile3, top2, tilesize):
                    rectangle = pygame.Rect(tile2, i, tilesize, tilesize)
                    self.tiles.append(rectangle)

    def rooms_by_row(self):
        # orders the rooms by row in a dictionary
        # 0: [*all_the_rooms_of_top_0], etc
        rooms_by_row = {}
        for i in range(0, self.dimensions[1], int(self.dimensions[1]/self.y_division)):
            rooms_by_row[i] = []
            for room in self.rooms:
                if room.top == i:
                    rooms_by_row[i].append(room)

        return rooms_by_row

    def join_all_rooms(self):
        """Joins all rooms horizontally and vertically"""


        # orders the rooms by row in a dictionary
        # 0: [*all_the_rooms_of_top_0], etc
        rooms_by_row = {}
        for i in range(0, self.dimensions[1], int(self.dimensions[1]/self.y_division)):
            rooms_by_row[i] = []
            for room in self.rooms:
                if room.top == i*st.GameSettings().tile_size:
                    rooms_by_row[i].append(room)


        # joins them together horizontally:
        for top in rooms_by_row.keys():
            for i in range(len(rooms_by_row[top])-1):
                self.join_rooms_h( rooms_by_row[top][i], rooms_by_row[top][i+1]  )

        # orders the rooms by column in a dictionary
        # 0: [*all_the_rooms_of_left_0], etc
        rooms_by_column = {}
        for i in range(0, self.dimensions[0], int(self.dimensions[0]/self.x_division)):
            rooms_by_column[i] = []
            for room in self.rooms:
                if room.left == i*st.GameSettings().tile_size:
                    rooms_by_column[i].append(room)

        # joins them together vertically:
        for left in rooms_by_column.keys():
            for i in range(len(rooms_by_column[left])-1):
                self.join_rooms_v( rooms_by_column[left][i], rooms_by_column[left][i+1]  )

    def get_edges_alt(self):
        """puts all edge tiles into the self.edges dictionary"""
        ts = self.tilesize

        for i in range(-ts, self.dimensions[0]*st.GameSettings().tile_size, self.tilesize):
            for j in range(-ts, self.dimensions[1]*st.GameSettings().tile_size, self.tilesize):

                # We cycle through all tiles
                if pygame.Rect(i,j,ts,ts) in self.tiles:
                    pass
                elif pygame.Rect(i+ts, j+ts, ts, ts) in self.tiles:
                    # up left
                    self.edges[(-1,1)].append(pygame.Rect(i,j,ts,ts))
                elif pygame.Rect(i+ts, j, ts, ts) in self.tiles:
                    # up 
                    self.edges[(0,1)].append(pygame.Rect(i,j,ts,ts))
                elif pygame.Rect(i+ts, j-ts, ts, ts) in self.tiles:
                    # up right
                    self.edges[(1,1)].append(pygame.Rect(i,j,ts,ts))
                elif pygame.Rect(i, j+ts, ts, ts) in self.tiles:
                    #  left
                    self.edges[(-1,0)].append(pygame.Rect(i,j,ts,ts))
                elif pygame.Rect(i, j-ts, ts, ts) in self.tiles:
                    # right
                    self.edges[(1,0)].append(pygame.Rect(i,j,ts,ts))
                elif pygame.Rect(i-ts, j+ts, ts, ts) in self.tiles:
                    # down left
                    self.edges[(-1,1)].append(pygame.Rect(i,j,ts,ts))
                elif pygame.Rect(i-ts, j, ts, ts) in self.tiles:
                    # down
                    self.edges[(-1,1)].append(pygame.Rect(i,j,ts,ts))
                elif pygame.Rect(i-ts, j-ts, ts, ts) in self.tiles:
                    # down right
                    self.edges[(-1,1)].append(pygame.Rect(i,j,ts,ts))

    def get_edges(self):
        """puts all edge tiles into the self.edges dictionary"""
        ts = self.tilesize

        for i in range(-ts, self.dimensions[0]*st.GameSettings().tile_size, self.tilesize):
            for j in range(-ts, self.dimensions[1]*st.GameSettings().tile_size, self.tilesize):

                edge = pygame.Rect(i,j,ts,ts)
                # We cycle through all tiles
                if edge in self.tiles:
                    pass
                elif len([rect for rect in gf.get_vicinity(edge) if rect in self.tiles]) == 0:
                    pass
                else:
                    key = random.choice([1,2,3])
                    self.edges[key].append(edge)

    def edges_to_list(self):
        for key in self.edges.keys():
            self.edges_list += self.edges[key]

    def render_rect(self, rect, tileset):
        """Given the rectangle of a room, and a tileset, renders the room"""
        # rect is the rect of the room
        # tileset are the sprites

        tilelenght = tileset.length
        width = rect.width
        height = rect.height
        for y in range(rect.top, rect.top+height, tilelenght):
            for x in range(rect.left, rect.left+width, tilelenght):
                self.screen.blit(tileset.image, (x,y), tileset.tiles[6])

    def render_dungeon_rooms(self, tileset):
        for room in self.rooms:
            self.render_rect(room, tileset)

    def render_edges_alt(self, edges, tileset):
        # Edges is a dict

        for key in edges.keys():
            for square in edges[key]:
                whatsquare = key[0]+1+(-key[1]+1)*5
                self.screen.blit(tileset.image, square, tileset.tiles[whatsquare])

    def render_edges_alt2(self, edges, tileset):
        # Edges is a dict

        for key in edges.keys():
            if key != -1:
                for square in edges[key]:
                    self.screen.blit(tileset.image, square, tileset.tiles[key])

    def render_dungeon(self, tileset):
        #for tile in self.tiles:
        #    self.screen.blit(tileset.image, tile, tileset.tiles[0])
        for edge in self.edges_list:
            self.screen.blit(tileset.image, edge, tileset.tiles[0])    

        #for tile in self.tiles:
        #   self.render_rect(tile, tileset)
        #self.render_edges(self.edges, tileset)

    def render_corpses(self):
        for corpse in self.corpses:
            self.screen.blit(pygame.image.load(st.SpritePaths().item_path), corpse.position)

    def recenter_dg(dungeon, chara):
        """Centers the character in some tile inside the dungeon"""
        # 1. given a position to start the character
        # 2. Moves the whole dungeon so that that position is the center

        chara_position = dungeon.choose_position() # absolute relative desired position
        screen_center = chara.rect # this is saved in chara position

        h_mov = chara_position.left - screen_center.left
        v_mov = chara_position.top - screen_center.top

        for game_object in dungeon.movables:
            game_object.centerx -= h_mov
            game_object.centery -= v_mov

    def reset_dungeon(self, chara):
        # Collection of the rooms as rects
        self.rooms = []
        # generates all the rooms
        self.generate()

        # All the walkable tiles in the dungeon
        self.tiles = []
        # joins all the rooms
        self.join_all_rooms()
        # puts all the room tiles into the self.tiles
        self.room_to_tiles()

        # All edge non-walkable tiles
        # Ex: { (-1,1) : all left upper corners, (-1,0) : all left walls, ....}
        self.edges = {}
        self.edges[-1] = []
        for i in range(25):
            self.edges[i] = []
        self.get_edges()

        self.edges_list=[]
        self.edges_to_list()

        # List of enemies
        self.enemies = enemies.generate_enemies(self)
        self.enemies_positions = []
        self.enemies_positions_to_list()

        self.items = game_items.generate_items(self)
        self.item_positions = []
        self.item_positions_to_list()

        self.stairs = game_items.Stairs(self.screen)
        self.stairs.position = self.choose_position()

        self.movables = (self.tiles + self.edges_list +
                    self.enemies_positions + self.item_positions +
                    [self.stairs.position]
                    )

        # List of corpses in the dungeon
        self.corpses = []
        self.corpses_positions = []

        self.recenter_dg(chara)

    def remove_enemy(self, enemy):
        st.SFX().enemy_death.play()
        self.enemies.remove(enemy)
        newcorpse = enemies.Corpse(enemy.position)
        self.corpses.append(newcorpse)
        self.corpses_positions.append(newcorpse.position)
        
        self.enemies_positions_to_list()

    def remove_corpse(self, corpse):
        self.corpses.remove(corpse)
        self.corpses_positions.remove(corpse.position)

    def remove_item(self, item):
        self.items.remove(item)
        self.item_positions_to_list()

    def new_get_edges(self):
        ts = st.GameSettings().tile_size

        for i in range(-ts, self.dimensions[0]*st.GameSettings().tile_size, self.tilesize):
            for j in range(-ts, self.dimensions[1]*st.GameSettings().tile_size, self.tilesize):

                # We cycle through all tiles
                if pygame.Rect(i,j,ts,ts) in self.tiles:
                    pass
                else:
                    pass

    def rect_to_enemy(self, rect):
        """Given a tile of the dungeon, it returns the enemy that is there"""
        
        for enemy in self.enemies:
            if enemy.position == rect:
                return enemy
        #If it doesnt find any, it returns None
    
    def rect_to_item(self, rect):
        """Given a tile of the dungeon, it returns the item that is there"""

        for item in self.items:
            if item.position == rect:
                return item

    def rect_to_corpse(self, rect):

        for corpse in self.corpses:
            if corpse.position == rect:
                return corpse

    def get_vicinity(rect) -> list:

        """Given a rectangle it returns all the rectangles around"""

        ts = st.GameSettings().tile_size

        #C = corner, u= upper, l= left, d=down, r= right
        cul = pygame.Rect(rect.left-ts, rect.top-ts, ts, ts)
        cur = pygame.Rect(rect.left+ts, rect.top-ts, ts, ts)
        cdl = pygame.Rect(rect.left-ts, rect.top+ts, ts, ts)
        cdr = pygame.Rect(rect.left+ts, rect.top+ts, ts, ts)

        #W = wall
        wu = pygame.Rect(rect.left, rect.top-ts, ts, ts)
        wd = pygame.Rect(rect.left, rect.top+ts, ts, ts)
        wl = pygame.Rect(rect.left-ts, rect.top, ts, ts)
        wr = pygame.Rect(rect.left+ts, rect.top, ts, ts)

        #These are all the squares around the rect
        return [cul, wu, cur, wl, wr, cdl, wd, cdr]
