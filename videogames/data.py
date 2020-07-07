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
        self.load_fx()

    def load_img(self):
        sprites = Spritesheet(path.join(self.img_folder, "spritesheet.png"))

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

        name = 'SPIDER'
        self.spider_img = sprites.image_at(
            MOBS[name]['IMG'][0],
            MOBS[name]['IMG'][1],
            TILESIZE,
            2,
            KEY_COLOR
        )

        # Weapons

        self.gun_img = pygame.image.load(path.join(self.img_folder, 
                                        WEAPONS['GUN']['IMG'])).convert_alpha()

        self.machinegun_img = pygame.image.load(path.join(self.img_folder, 
                                        WEAPONS['MACHINEGUN']['IMG'])).convert_alpha()
        
        self.shotgun_img = pygame.image.load(path.join(self.img_folder, 
                                        WEAPONS['SHOTGUN']['IMG'])).convert_alpha()

        self.deagle_img = pygame.image.load(path.join(self.img_folder, 
                                        WEAPONS['DEAGLE']['IMG'])).convert_alpha()

        self.assault_img = pygame.image.load(path.join(self.img_folder, 
                                        WEAPONS['ASSAULT']['IMG'])).convert_alpha()

    def load_fx(self):

        self.walk_fx = []
        walk_list = list(range(0, 10))
        for step in walk_list:
            fx = pygame.mixer.Sound(
                path.join(self.fx_folder, f'step{step}.ogg'))
            self.walk_fx.append(fx)

        self.gun_sound = pygame.mixer.Sound(
            path.join(self.fx_folder, WEAPONS['GUN']['FX']))