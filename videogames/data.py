from os import path

import pygame

from settings import *
from spritesheet import Spritesheet


class Data():
    def __init__(self):
        pygame.mixer.pre_init(44100, -16, 2, 1024)
        pygame.init()
        pygame.mixer.init()
        pygame.mixer.set_num_channels(16)
        self.screen = pygame.display.set_mode([WIDTH, HEIGHT])
        self.root_folder = path.dirname(__file__)
        self.img_folder = path.join(self.root_folder, "img")
        self.fx_folder = path.join(self.root_folder, "fx")
        self.load_img()

    def load_img(self):
        spritesheet_path = path.join(self.img_folder, "spritesheet.png")
        sprites = Spritesheet(spritesheet_path)

        # Items

        self.healthpack_img = sprites.image_at(
            ITEMS['HEALTHPACK']['IMG'][0],
            ITEMS['HEALTHPACK']['IMG'][1],
            TILESIZE,
            2,
            KEY_COLOR
        )

        self.speedup_img = sprites.image_at(
            ITEMS['SPEEDUP']['IMG'][0],
            ITEMS['SPEEDUP']['IMG'][1],
            TILESIZE,
            2,
            KEY_COLOR
        )

        # Mobs
        name = 'PLAYER'
        self.player_img = sprites.image_at(
            MOBS[name]['IMG'][0],
            MOBS[name]['IMG'][1],
            TILESIZE,
            2,
            KEY_COLOR
        )

        name = 'BEE'
        self.bee_img = sprites.image_at(
            MOBS[name]['IMG'][0],
            MOBS[name]['IMG'][1],
            TILESIZE,
            2,
            KEY_COLOR
        )

        name = 'BEE_NEST'
        self.bee_nest_img = sprites.image_at(
            MOBS[name]['IMG'][0],
            MOBS[name]['IMG'][1],
            TILESIZE,
            2,
            KEY_COLOR
        )

        name = 'TOWER'
        self.tower_img = sprites.image_at(
            MOBS[name]['IMG'][0],
            MOBS[name]['IMG'][1],
            TILESIZE,
            2,
            KEY_COLOR
        )

        # Floor and walls
        self.floor_img = sprites.image_at(
                    FLOOR_SPRITE[0],
                    FLOOR_SPRITE[1],
                    TILESIZE,
                    2,
                    KEY_COLOR
        )

        self.wall_img = sprites.image_at(
                    WALL_SPRITE[0],
                    WALL_SPRITE[1],
                    TILESIZE,
                    2,
                    KEY_COLOR
        )

    def load_fx(self):

        self.walk_fx = []
        walk_list = list(range(0, 10))
        for step in walk_list:
            fx = pygame.mixer.Sound(
                path.join(self.fx_folder, f'step{step}.ogg'))
            self.walk_fx.append(fx)

        self.gun_sound = pygame.mixer.Sound(
            path.join(self.fx_folder, WEAPONS['GUN']['FX']))


# TEST

# data = Data()

# while True:
#     print('Reproduciendo')
#     for i in range(len(data.walk_fx)):
#         data.walk_fx[i].play()
#         pygame.time.delay(300) # good time
