import random
from os import path

from pygame import Vector2

from data import Data
from settings import *
from sprites import *


class Map():

    ''' Map Class. You have 3 ways of map generation:
    1) Loading from a txt file
    2) Carve Cave Cellular Automata way (procedural)
    3) Carve Cave Drunken Diggers (procedural)
    # We are currently using the third way.
    # You can modify this on game.py - load and reload functions '''

    def __init__(self):
        self.map_data = []
        self.data = Data()
        self.player_entry_point = Vector2(0, 0)

    def load_from_file(self, filename):
        
        ''' Loading map from a txt file '''
        
        game_folder = path.dirname(__file__)
        data_folder = path.join(game_folder, 'data')
        with open(path.join(data_folder, filename), 'r') as file:
            for line in file:
                self.map_data.append(line)

    def carve_cave_cellular_automata(self, game, screen_width, screen_height):

        ''' Procedural way of creating a map, using mathemathical model 
        of cellular automata theory. At the end, you call the smooth_map function'''

        width = screen_width // TILESIZE
        height = screen_height // TILESIZE
        self.width = width
        self.height = height

        self.map_data = [['1' if y == 0 or y == (height-1) or x == 0 or x == (
            width - 1) else '0' for x in range(0, width)] for y in range(0, height)]

        starting_walls = (int)(width * height * 0.4)
        for _ in range(0, starting_walls):
            x = random.randint(1, width - 1)
            y = random.randint(1, height - 1)
            self.map_data[y][x] = "1"

        iterations = 10
        self.smooth_map(iterations, width, height)

    def smooth_map(self, iterations, width, height):

        ''' Smoothing map function '''

        neighbour_deltas = [(x, y) for x in range(-1, 2)
                            for y in range(-1, 2) if x != 0 or y != 0]
        for _ in range(iterations):
            tmp_map = self.map_data.copy()
            for x in range(1, width - 1):
                for y in range(1, height - 1):
                    sum = 0
                    for delta in neighbour_deltas:
                        dx, dy = delta
                        if self.map_data[y + dy][x + dx] == "1":
                            sum += 1
                    if tmp_map[y][x] == "1":
                        tmp_map[y][x] = "1" if sum >= 3 else "0"
                    else:
                        tmp_map[y][x] = "1" if sum >= 5 else "0"
            self.map_data = tmp_map.copy()

    def carve_cave_drunken_diggers(self, game, screen_width, screen_height):

        ''' Dungeon generation algorithm that makes sure 
        to connect all rooms on the map '''

        width = screen_width // TILESIZE
        height = screen_height // TILESIZE
        self.width = width
        self.height = height

        self.map_data = [['1' for x in range(0, width)]
                         for y in range(0, height)]

        iterations = (int)(width * height * 0.45)
        digger_count = 5
        diggers = [Vector2(width//2, height//2) for i in range(digger_count)]
        neighbour_deltas = [(-1, 0), (0, 1), (1, 0), (0, -1)]

        for _ in range(iterations):
            tmp_map = self.map_data.copy()
            for i in range(digger_count):
                direction = random.choice(neighbour_deltas)

                diggers[i] = diggers[i] + direction
                if diggers[i].x < 1:
                    diggers[i].x = 1
                if diggers[i].y < 1:
                    diggers[i].y = 1
                if diggers[i].x > width - 2:
                    diggers[i].x = width - 2
                if diggers[i].y > height - 2:
                    diggers[i].y = height - 2
                tmp_map[int(diggers[i].y)][int(diggers[i].x)] = "0"

            self.map_data = tmp_map.copy()

    def get_empty_position(self):

        ''' Looks for an empty position on the map '''

        is_empty = False
        while is_empty == False:
            x = random.randint(1, self.width - 1)
            y = random.randint(1, self.height - 1)
            if self.map_data[y][x] == "0":
                return (x, y)

    def create_sprites_from_map_data(self, game):

        ''' Mob, player, items and weapons generation '''

        for row, tiles in enumerate(self.map_data):
            for col, tile in enumerate(tiles):
                position = Vector2(col, row) * TILESIZE

                # Walls
                if tile == '1':
                    Wall(game, col, row)
                
                # Player (only entry point)
                if tile == 'P':
                    self.player_entry_point = position

                # Bees
                if tile == "b":
                    name = 'BEE'
                    Bee(
                        game,
                        position,
                        MOBS[name]['MAX_SPEED'],
                        MOBS[name]['ACCELERATION'],
                        MOBS[name]['HEALTH'],
                        MOBS[name]['HIT_DAMAGE'],
                        self.data.bee_img
                    )

                # Deprecated bee nests
                if tile == "B":
                    name = 'BEE_NEST'
                    BeeNest(
                        game,
                        position,
                        MOBS[name]['HEALTH'],
                        MOBS[name]['SPAWN_FREQUENCY'] + randint(2000, 5000),
                        MOBS[name]['MAX_POPULATION'],
                        self.data.bee_nest_img
                    )

                # Spiders
                if tile == "X":
                    name = 'SPIDER'
                    Spider(game,
                           position,
                           MOBS[name]['MAX_SPEED'],
                           MOBS[name]['ACCELERATION'],
                           MOBS[name]['HEALTH'],
                           MOBS[name]['HIT_DAMAGE'],
                           self.data.spider_img
                           )

                # Towers
                if tile == "T":
                    Tower(
                        game,
                        position,
                        self.data.tower_img
                    )

                # Items
                if tile == "h":
                    HealthPack(game, position)
                    
                if tile == "s":
                    SpeedUp(game, position)

                # Weapons
                if tile == "M":
                    Machinegun(game, position)

                if tile == "S":
                    Shotgun(game, position)

                if tile == "D":
                    Deagle(game, position)

                if tile == "A":
                    Assault(game, position)
