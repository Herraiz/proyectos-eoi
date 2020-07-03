from os import path

import pygame

from settings import *
from spritesheet import Spritesheet

class Data():
    def __init__(self):
        pygame.mixer.pre_init(44100, -16, 2,1024)
        pygame.init()
        pygame.mixer.init()
        pygame.mixer.set_num_channels(16)
        self.screen = pygame.display.set_mode([WIDTH, HEIGHT])
        self.root_folder = path.dirname(__file__)
        self.img_folder = path.join(self.root_folder, "img")
        self.fx_folder = path.join(self.root_folder, "fx")
        self.load_img() #test

    def load_img(self):
        spritesheet_path = path.join(self.img_folder, "spritesheet.png")
        self.spritesheet = Spritesheet(spritesheet_path)
        self.colorkey = (94, 129, 162)
        
        self.bee_img = self.spritesheet.image_at(556, 258, 573, 272, self.colorkey)
        # print('todo va bien')

    def load_fx(self):

        self.walk_fx = []
        walk_list = list(range(0,10))
        for step in walk_list:
            fx = pygame.mixer.Sound(path.join(self.fx_folder, f'step{step}.ogg'))
            self.walk_fx.append(fx)

        self.gun_sound = pygame.mixer.Sound(path.join(self.fx_folder, WEAPONS['GUN']['FX']))
        

# TEST

# data = Data()

# while True:
#     print('Reproduciendo')
#     for i in range(len(data.walk_fx)):
#         data.walk_fx[i].play()
#         pygame.time.delay(300) # good time