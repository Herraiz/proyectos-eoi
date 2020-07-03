# colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (200, 100, 100)
GREEN = (100, 200, 100)
DARKGREEN = (10, 20, 10)
BLUE = (100, 100, 200)
DARKBLUE = (25, 25, 50)
YELLOW = (200, 200, 100)
ORANGE = (200, 150, 100)
DARKORANGE = (100, 75, 50)
PURPLE = (182, 56, 157)
DARKGREY = (45, 45, 45)
GROUND = (201, 152, 105)
WALL = (49, 36, 26)

# game settings
WIDTH = 1428
HEIGHT = 882
FPS = 60
GAME_TITLE = "Pew Pew Pew"

# map
TILESIZE = 42
KEY_COLOR = (94, 129, 162)

DRAG = 10
AVOID_RADIUS = 50

PLAYER_MAX_SPEED = 100
PLAYER_ACCELERATION = 2000
PLAYER_HEALTH = 100

BEE_MAX_SPEED = 50
BEE_ACCELERATION = 10000
BEE_HEALTH = 10
BEE_HIT_DAMAGE = 10
BEE_VISION_RADIUS = 150

BEE_NEST_SPAWN_FREQUENCY = 5000
BEE_NEST_MAX_POPULATION = 5
BEE_NEST_HEALTH = 100

MOBS = {
    'PLAYER': {
        'HEALTH': 100,
        'IMG': (19, 3),
        'WEAPON_NAME': 'GUN',
        'MAX_SPEED': 100,
        'ACCELERATION': 2000,
    },

    'BEE': {
        'HEALTH': 10,
        'IMG': (24, 11),
        'HIT_DAMAGE': 10,
        'MAX_SPEED': 50,
        'ACCELERATION': 10000,
        'VISION_RADIUS': 150,
        },

    'BEE_NEST': {
        'HEALTH': 100,
        'IMG': (26, 28),
        'MAX_POPULATION': 5,
        'SPAWN_FREQUENCY': 5000,
    },

    'TOWER': {
        'HEALTH': 100,
        'WEAPON_NAME': 'GUN',
        'IMG': (28, 23)
    },
}


ITEM_HOVER_SPEED = 0.01

ITEMS = {
    'HEALTHPACK': {
        'HEAL': 20,
        'IMG': (13,12),
        'FX': 'heal.wav',
    },

    'SPEEDUP': {
        'SPEED': 50,
        'TTL': 3000,
        'IMG': (6, 29),
    }
}

WEAPONS = {
    'GUN': {
        'FIRING_RATE': 250,
        'SPREAD': 0.1,
        'TTL':  2000,
        'SPEED': 300,
        'DAMAGE': 5,
        'COLOR': RED,
        'SIZE': 10,
        'AMMO_PER_SHOT': 1,
        'FX': "pew.wav"
    },
        'MACHINEGUN': {
        'FIRING_RATE': 100,
        'SPREAD': 0.1,
        'TTL':  1500,
        'SPEED': 300,
        'DAMAGE': 2,
        'COLOR': RED,
        'SIZE': 8,
        'AMMO_PER_SHOT': 1,
        'FX': "papapapa.wav"
    },
        'SHOTGUN': {
        'FIRING_RATE': 2000,
        'SPREAD': 0.5,
        'TTL':  500,
        'SPEED': 300,
        'DAMAGE': 10,
        'COLOR': RED,
        'SIZE': 8,
        'AMMO_PER_SHOT': 10,
        'FX': "kaboom.wav"
    },
        'DEAGLE': {
        'FIRING_RATE': 100,
        'SPREAD': 0.1,
        'TTL':  2000,
        'SPEED': 300,
        'DAMAGE': 25,
        'COLOR': RED,
        'SIZE': 10,
        'AMMO_PER_SHOT': 1,
        'FX': "kaboom.wav"
    },
}

FLOOR_SPRITE =  (7, 23)
WALL_SPRITE = (2, 3)