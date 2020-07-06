import pygame
from settings import *
from sprites import *
from map import Map
from data import Data


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption(GAME_TITLE)
        self.screen = pygame.display.set_mode([WIDTH, HEIGHT])
        self.clock = pygame.time.Clock()

        self.large_font = pygame.font.SysFont('arial', 100)
        self.small_font = pygame.font.SysFont("arial", 32)

        self.data = Data()
        self.map = Map()

        self.player = None
        self.player_current_weapon = 'GUN'
        self.player_current_weapon_img = self.data.gun_img

        self.playing = False
        self.main_menu()

    def load_data(self):
        self.all_sprites = pygame.sprite.Group()
        self.walls = pygame.sprite.Group()
        self.floor = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()
        self.mobs = pygame.sprite.Group()
        self.nests = pygame.sprite.Group()
        self.items = pygame.sprite.Group()
        self.players = pygame.sprite.Group()

        # self.map.load_from_file('map.txt')
        # self.map.carve_cave_cellular_automata(self, WIDTH, HEIGHT)
        self.map.carve_cave_drunken_diggers(self, WIDTH, HEIGHT)

        self.populate_map()

        self.map.create_sprites_from_map_data(self)


        self.player = Player(self, self.map.player_entry_point,
                    PLAYER_MAX_SPEED, PLAYER_ACCELERATION,
                    PLAYER_HEALTH, self.data.player_img, self.map, 
                    self.player_current_weapon, 
                    self.player_current_weapon_img)

    def reload_data(self):
        self.all_sprites = pygame.sprite.Group()
        self.walls = pygame.sprite.Group()
        self.floor = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()
        self.mobs = pygame.sprite.Group()
        self.nests = pygame.sprite.Group()
        self.items = pygame.sprite.Group()

        # self.map.load_from_file('map.txt')
        # self.map.carve_cave_cellular_automata(self, WIDTH, HEIGHT)
        self.map.carve_cave_drunken_diggers(self, WIDTH, HEIGHT)

        self.populate_map()

        self.map.create_sprites_from_map_data(self)

        self.player.respawn(self.map.player_entry_point)




    def populate_map(self):
        print(f'{self.player_current_weapon}')

        # Player
        x, y = self.map.get_empty_position()
        self.map.map_data[y][x] = "P"

        # Bees
        increase_bees = round(self.level * 0.3)
        for _ in range(4 + increase_bees):
            x, y = self.map.get_empty_position()
            self.map.map_data[y][x] = "b"

        # Tower
        increase_towers = round(self.level * 0.1)
        for _ in range(1 + increase_towers):
            x, y = self.map.get_empty_position()
            self.map.map_data[y][x] = "T"

        increase_utility = round(self.level * 0.03)

        # HealthPack
        for _ in range(1 + increase_utility):
            x, y = self.map.get_empty_position()
            self.map.map_data[y][x] = "h"

        # SpeedUp
        for _ in range(1 + increase_utility):
            x, y = self.map.get_empty_position()
            self.map.map_data[y][x] = "s"

        ## Weapons

        # Machinegun
        if self.level >= 6 and self.level <= 9:
            x, y = self.map.get_empty_position()
            self.map.map_data[y][x] = "M"
    
        # Shotgun
        if self.level >= 10 and self.level <= 14:
            x, y = self.map.get_empty_position()
            self.map.map_data[y][x] = "S"

        # Deagle
        if self.level >= 15 and self.level <= 19:
            x, y = self.map.get_empty_position()
            self.map.map_data[y][x] = "D"  

        # Assault
        if self.level >= 15:
            x, y = self.map.get_empty_position()
            self.map.map_data[y][x] = "A" 


    def start_game(self):
        self.level = 20
        self.score = 0
        self.load_data()
        self.run()

    def next_level(self):
        self.level += 1
        self.reload_data()
        self.run()

    def run(self):
        self.playing = True
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000
            self.events()
            self.update()
            self.draw()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

    def update(self):
        self.players.update()
        self.floor.update()
        self.walls.update()
        self.mobs.update()
        self.items.update()
        self.bullets.update()

        if len(self.mobs) == 0:
            self.next_level()

    def draw(self):

        self.screen.fill(GROUND)
        self.players.draw(self.screen)
        self.floor.draw(self.screen)
        self.walls.draw(self.screen)
        self.mobs.draw(self.screen)
        self.items.draw(self.screen)
        self.bullets.draw(self.screen)

        for mob in self.mobs:
            mob.draw_health()

        self.draw_game_ui()

        pygame.display.update()

    def draw_game_ui(self):

        # Health
        health = self.player.health / self.player.max_health
        padding = 3
        width = 100
        height = 25
        health_background = pygame.Rect(10, 10, width, height)
        bar_width = int(health * (width - padding*2))
        health_fill = pygame.Rect(
            10 + padding, 10 + padding, bar_width, height - padding*2)
        pygame.draw.rect(self.screen, DARKBLUE, health_background)
        pygame.draw.rect(self.screen, BLUE, health_fill)

        # Score
        score_text = self.small_font.render(
            f'- Score: {self.score}', True, WHITE)
        self.screen.blit(score_text, (width + 173, 4))

        # Level
        level_text = self.small_font.render(
            f'- Level: {self.level}', True, WHITE)
        self.screen.blit(level_text, (width + 22, 4))

        # Weapon
        self.screen.blit(self.player.weapon_img, (5, HEIGHT - 47))

    def main_menu(self):
        title_text = self.large_font.render('MOUNTAIN PEW', True, YELLOW)
        instructions_text = self.small_font.render(
            "Press any key to START", True, WHITE)

        self.screen.fill(DARKGREY)
        self.screen.blit(title_text,
                         (WIDTH // 2 - title_text.get_rect().width // 2,
                          HEIGHT - 550 - title_text.get_rect().height // 2))

        self.screen.blit(instructions_text,
                         (WIDTH // 2 - instructions_text.get_rect().width // 2,
                          HEIGHT - 300))

        pygame.display.flip()

        in_main_menu = True

        while in_main_menu:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    in_main_menu = False
                    self.start_game()

    def game_over(self):
        # pygame.mixer.music.stop()
        # self.game_over_fx.play()
        title_text = self.large_font.render('GAME OVER', True, YELLOW)
        score_text = self.small_font.render(
            f"Score: {self.score} [Press any key]", True, WHITE)

        self.screen.fill(DARKGREY)
        self.screen.blit(title_text,
                         (WIDTH // 2 - title_text.get_rect().width // 2,
                          HEIGHT - 550 - title_text.get_rect().height // 2))

        self.screen.blit(score_text,
                         (WIDTH // 2 - score_text.get_rect().width // 2,
                          HEIGHT - 300))

        pygame.display.flip()

        in_game_over = True
        pygame.time.delay(3000)
        while in_game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    in_game_over = False
                    self.main_menu()


game = Game()
game.main_menu()
