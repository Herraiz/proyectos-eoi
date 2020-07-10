# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (200, 100, 100)
GREEN = (50, 200, 50)
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

# Game Settings
GAME_TITLE = "Mountain Pew"
WIDTH = 1428
HEIGHT = 882
FPS = 60


# Map
TILESIZE = 42
KEY_COLOR = (94, 129, 162)

# Generic FX / IMG
MENU_SELECTION_FX = 'selection.wav'

MENU_IMG = 'main_menu.png'

GAME_OVER_IMG = 'game_over.png'

MUSIC_LOOP = 'music_loop.mp3'

DEAD_FX = 'dead.wav'


DRAG = 10
AVOID_RADIUS = 50


MOBS = {
    'PLAYER': {
        'HEALTH': 100,
        'IMG': (19, 0),
        'WEAPON_NAME': 'GUN',
        'MAX_SPEED': 125,
        'ACCELERATION': 2000,
    },

    'BEE': {
        'HEALTH': 10,
        'IMG': (24, 11),
        'MAX_SPEED': 50,
        'ACCELERATION': 10000,
        'HIT_DAMAGE': 10,
        'VISION_RADIUS': 250,
        },

    'BEE_NEST': {
        'HEALTH': 100,
        'IMG': (26, 28),
        'MAX_POPULATION': 5,
        'SPAWN_FREQUENCY': 5000,
    },

    'TOWER': {
        'HEALTH': 100,
        'WEAPON_NAME': 'TOWER_TURRET',
        'VISION_RADIUS': 300,
        'IMG': (28, 23),
        'MAX_SPEED': 0,
        'ACCELERATION': 0
    },

    'SPIDER': {
        'HEALTH': 100,
        'IMG': (20, 15),
        'HIT_DAMAGE': 25,
        'MAX_SPEED': 25,
        'ACCELERATION': 1000,
        'VISION_RADIUS': 250,
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
        'SPEED': 50, # 50
        'TTL': 5000,
        'IMG': (6, 29),
        'FX': 'powerup.wav',
    }
}

WEAPONS = {

    'GENERIC': {
        'FX': "weapon_pickup.wav",
    },

    'GUN': {
        'FIRING_RATE': 250,
        'SPREAD': 0.1,
        'TTL':  1500,
        'SPEED': 300,
        'DAMAGE': 10,
        'COLOR': RED,
        'SIZE': 10,
        'AMMO_PER_SHOT': 1,
        'FX': "pew.wav",
        'IMG': "gun.png"
    },
    'MACHINEGUN': {
        'FIRING_RATE': 100,
        'SPREAD': 0.1,
        'TTL':  1500,
        'SPEED': 400,
        'DAMAGE': 5,
        'COLOR': RED,
        'SIZE': 8,
        'AMMO_PER_SHOT': 1,
        'IMG': "machinegun.png"
    },
    'SHOTGUN': {
        'FIRING_RATE': 750,
        'SPREAD': 0.5,
        'TTL':  1000,
        'SPEED': 300,
        'DAMAGE': 10,
        'COLOR': RED,
        'SIZE': 8,
        'AMMO_PER_SHOT': 10,
        'IMG': "shotgun.png"
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
        'IMG': "deagle.png"
    },

    'ASSAULT': {
        'FIRING_RATE': 100,
        'SPREAD': 0.1,
        'TTL':  2000,
        'SPEED': 300,
        'DAMAGE': 10,
        'COLOR': RED,
        'SIZE': 10,
        'AMMO_PER_SHOT': 1,
        'IMG': "assault.png"
    },

    'TOWER_TURRET': {
        'FIRING_RATE': 750,
        'SPREAD': 0.1,
        'TTL':  2000,
        'SPEED': 200,
        'DAMAGE': 10,
        'COLOR': YELLOW,
        'SIZE': 15,
        'AMMO_PER_SHOT': 1,
    },
}