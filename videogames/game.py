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

        self.map = Map()
        # self.map.load_from_file('map.txt')
        # self.map.carve_cave_cellular_automata(self, WIDTH, HEIGHT)
        self.map.carve_cave_drunken_diggers(self, WIDTH, HEIGHT)
        self.populate_map()

        self.map.create_sprites_from_map_data(self)

        self.player = Player(self, self.map.player_entry_point,
                             PLAYER_MAX_SPEED, PLAYER_ACCELERATION,
                             PLAYER_HEALTH, self.data.player_img)

    def populate_map(self):
        for _ in range(3):
            x, y = self.map.get_empty_position()
            self.map.map_data[y][x] = "B"
            # self.map.create_empty_square(y, x)

        x, y = self.map.get_empty_position()
        self.map.map_data[y][x] = "P"

        x, y = self.map.get_empty_position()
        self.map.map_data[y][x] = "h"

        x, y = self.map.get_empty_position()
        self.map.map_data[y][x] = "s"

        x, y = self.map.get_empty_position()
        self.map.map_data[y][x] = "T"

    def start_game(self):
        self.load_data()
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
        self.all_sprites.update()

        if len(self.mobs) == 0:
            pygame.time
            pygame.time.delay(1000)
            self.start_game()


        if len(self.players) == 0:
            print('You lose!')

    def draw(self):
        self.screen.fill(GROUND)

        # self.all_sprites.draw(self.screen)

        # Draw order:
        self.floor.draw(self.screen)
        self.walls.draw(self.screen)
        self.mobs.draw(self.screen)
        self.items.draw(self.screen)
        self.bullets.draw(self.screen)
        self.players.draw(self.screen)
        # Another way: http://www.pygame.org/docs/ref/sprite.html#pygame.sprite.OrderedUpdates

        for mob in self.mobs:
            mob.draw_health()
            # debug
            # pygame.draw.line(self.screen, RED, mob.position,
            #                  mob.position + mob.avoidance * 5, 3)

            # pygame.draw.line(self.screen, BLUE, mob.position,
            #                  mob.position + mob.desired_velocity * 5, 3)
            # debug

        self.draw_game_ui()

        pygame.display.flip()

    def draw_game_ui(self):
        # health_text = self.small_font.render('Health:', True, BLUE)
        # self.screen.blit(health_text, (10, 10))

        health = self.player.health / self.player.max_health
        padding = 3
        width = 100
        height = 25

        health_background = pygame.Rect(5, 5, width, height)
        bar_width = int(health * (width - padding*2))
        health_fill = pygame.Rect(
            5 + padding, 5 + padding, bar_width, height - padding*2)
        pygame.draw.rect(self.screen, DARKBLUE, health_background)
        pygame.draw.rect(self.screen, BLUE, health_fill)


    def main_menu(self):
            title_text = self.large_font.render('MOUNTAIN PEW', True, YELLOW)
            instructions_text = self.small_font.render("Press any key to START", True, WHITE)

            self.screen.fill(DARKGREY)
            self.screen.blit(title_text,
                            (WIDTH // 2 - title_text.get_rect().width // 2,
                            HEIGHT // 2  - title_text.get_rect().height // 2))

            self.screen.blit(instructions_text,
                            (WIDTH // 2 - instructions_text.get_rect().width // 2,
                            HEIGHT - 64))


            pygame.display.flip()
            # pygame.time.delay(1000)

            in_main_menu = True

            while in_main_menu:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        quit()
                    if event.type == pygame.KEYDOWN:
                        in_main_menu = False
                        self.start_game()
                        # pygame.time.delay(500)


game = Game()
game.main_menu()
