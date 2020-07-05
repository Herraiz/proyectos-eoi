from random import randint, uniform
import math

import pygame
from pygame import Vector2

from settings import *
from data import Data


class Wall(pygame.sprite.Sprite):
    def __init__(self, game, x, y, image):
        self.groups = game.all_sprites, game.walls
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pygame.Surface((TILESIZE, TILESIZE))
        self.image.fill(WALL)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE


class Floor(pygame.sprite.Sprite):
    def __init__(self, game, x, y, image):
        self.groups = game.all_sprites, game.floor
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = image
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE


class Mob(pygame.sprite.Sprite):
    def __init__(self, game, groups, position, max_speed,
                 acceleration, max_health, image):

        self.groups = groups
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.data = Data()
        self.image = image
        self.rect = self.image.get_rect()

        self.max_speed = max_speed + \
            uniform(-max_speed * 0.25, max_speed * 0.25)
        self.acceleration = acceleration
        self.position = position
        self.rect.topleft = position
        self.desired_velocity = Vector2(0, 0)
        self.velocity = Vector2(0, 0)
        self.avoidance = Vector2(0, 0)
        self.max_health = max_health
        self.health = max_health

        self.last_shot_time = 0  # TODO: ESTO IRÁ EN LA CLASS WEAPON FUTURA

    def update(self):
        pass

    def move(self):
        if self.desired_velocity.magnitude() > 0:
            self.desired_velocity = self.desired_velocity.normalize()

        self.velocity -= self.velocity * DRAG * self.game.dt
        self.velocity += (self.desired_velocity + self.avoidance) * \
            self.acceleration * self.game.dt
        if self.velocity.magnitude() > self.max_speed:
            self.velocity.scale_to_length(self.max_speed)

        self.position += self.velocity * self.game.dt

        self.rect.x = self.position.x
        self.collide_with_walls('x')
        self.rect.y = self.position.y
        self.collide_with_walls('y')

    def collide_with_walls(self, dir):
        hits = pygame.sprite.spritecollide(self, self.game.walls, False)
        if len(hits) == 0:
            return

        if dir == 'x':
            if self.velocity.x > 0:
                self.position.x = hits[0].rect.left - self.rect.width
            if self.velocity.x < 0:
                self.position.x = hits[0].rect.right
            self.velocity.x = 0
            self.rect.x = self.position.x

        if dir == 'y':
            if self.velocity.y > 0:
                self.position.y = hits[0].rect.top - self.rect.height
            if self.velocity.y < 0:
                self.position.y = hits[0].rect.bottom
            self.velocity.y = 0
            self.rect.y = self.position.y


    def receive_damage(self, damage):
        self.health -= damage
        if self.health <= 0:
            self.health = 0
            self.kill()

    def draw_health(self):
        health = self.health / self.max_health
        bar_width = int(health * self.rect.width)
        health_bar = pygame.Rect(
            self.position.x, self.position.y - 7, bar_width, 5)
        pygame.draw.rect(self.game.screen, GREEN, health_bar)

    def avoid_mobs(self):
        towards_mobs = Vector2(0, 0)
        for mob in self.game.mobs:
            if mob != self:
                towards_mob = mob.position - self.position
                if 0 < towards_mob.magnitude() < AVOID_RADIUS:
                    towards_mobs += towards_mob / towards_mob.magnitude()

        # self.avoidance = self.avoidance.lerp(-towards_mobs, self.game.dt) #TODO: No funciona con bees


    def shoot_at(self, x, y, target_group):
        weapon = WEAPONS[self.weapon_name]

        time_since_last_shot = pygame.time.get_ticks() - self.last_shot_time
        if time_since_last_shot < weapon['FIRING_RATE']:
            return
        bullet_velocity = Vector2(x, y) - self.position
        if bullet_velocity.magnitude() > 0:
            bullet_velocity = bullet_velocity.normalize()

        for _ in range(weapon['AMMO_PER_SHOT']):
            Bullet(
                self.game,
                Vector2(self.rect.center),
                bullet_velocity,
                weapon['SPREAD'],
                weapon['TTL'],
                weapon['SPEED'],
                weapon['DAMAGE'],
                weapon['COLOR'],
                weapon['SIZE'],
                target_group
            )
            self.data.gun_sound.play() # TODO: SOUND
        self.last_shot_time = pygame.time.get_ticks()


class Player(Mob):
    def __init__(self, game, position, max_speed,
                 acceleration, max_health, image, map):

        super().__init__(game, (game.all_sprites, game.players), position,
                         max_speed, acceleration, max_health, image)
        self.map = map
        self.max_speed = max_speed
        self.weapon_name = 'DEAGLE'

    def update(self):
        self.handle_input()
        self.move()

        # teleport player if is outside the window
        if self.position.x > WIDTH or self.position.x < 0:
            self.position.x, self.position.y = self.map.get_empty_position()
        if self.position.y > HEIGHT or self.position.y <0:
            self.position.x, self.position.y = self.map.get_empty_position()

    def handle_input(self):

        mouse = pygame.mouse.get_pressed()
        if mouse[0] or mouse[0] or mouse[0]:
            x, y = pygame.mouse.get_pos()
            self.shoot_at(x, y, self.game.mobs)

        vx, vy = 0, 0
        key = pygame.key.get_pressed()
        if key[pygame.K_a]:
            vx = -1
        if key[pygame.K_d]:
            vx = 1
        if key[pygame.K_w]:
            vy = -1
        if key[pygame.K_s]:
            vy = 1

        self.desired_velocity = Vector2(vx, vy)


class Bee(Mob):
    def __init__(self, game, position, max_speed,
                 acceleration, max_health, damage, image, groups=()):

        super().__init__(game, (game.all_sprites, game.mobs) + groups,
                         position, max_speed, acceleration, max_health, image)

        self.damage = damage

    def update(self):
        towards_player = self.game.player.position - self.position
        if towards_player.magnitude() <= BEE_VISION_RADIUS:
            self.desired_velocity = towards_player
        else:
            self.desired_velocity = Vector2(uniform(-1, 1),
                                            uniform(-1, 1))
        self.avoid_mobs()
        self.move()
        if pygame.sprite.collide_rect(self, self.game.player):
            self.game.player.receive_damage(self.damage * self.game.dt)

        # Kill the mobs outside the window
        if self.position.x > WIDTH or self.position.x < 0:
            self.kill()
        if self.position.y > HEIGHT or self.position.y <0:
            self.kill()
        
    def receive_damage(self, damage):
        self.health -= damage
        if self.health <= 0:
            self.health = 0
            self.game.score += 10
            self.kill()


class BeeNest(Mob):
    def __init__(self, game, position, max_health, spawn_frequency, max_population, image):
        super().__init__(game, (game.all_sprites, game.nests,
                                game.mobs), position, 0, 0, max_health, image)

        self.spawn_frequency = spawn_frequency
        self.last_spawn_time = 0
        self.max_population = max_population
        self.population = pygame.sprite.Group()

    def update(self):
        time_since_last_spawn = pygame.time.get_ticks() - self.last_spawn_time
        time_has_passed = time_since_last_spawn >= self.spawn_frequency
        room_left = len(self.population) < self.max_population

        if time_has_passed and room_left:
            max_spawneable = self.max_population - len(self.population)
            to_spawn = randint(1, max_spawneable)
            for _ in range(to_spawn):
                Bee(
                    self.game,
                    Vector2(self.position.x, self.position.y) +
                    Vector2(uniform(-TILESIZE, TILESIZE),
                            uniform(-TILESIZE, TILESIZE)),
                    BEE_MAX_SPEED,
                    BEE_ACCELERATION,
                    BEE_HEALTH,
                    BEE_HIT_DAMAGE,
                    self.data.bee_img,
                    (self.population,)
                )
            self.last_spawn_time = pygame.time.get_ticks()

    def receive_damage(self, damage):
        self.health -= damage
        if self.health <= 0:
            self.health = 0
            self.game.score += 30
            self.kill()

class Tower(Mob):
    def __init__(self, game, position, image):
        max_health = MOBS['TOWER']['HEALTH']
        super().__init__(game, (game.all_sprites, game.mobs),
                         position, 0, 0, max_health, image)

        self.weapon_name = MOBS['TOWER']['WEAPON_NAME']

    def update(self):
        towards_player = self.game.player.position - self.position
        target = self.game.player.position

        if 0 < towards_player.magnitude() < 200:     # TODO: VISION RADIUS, RANGE
            self.shoot_at(target.x, target.y, self.game.players)
    
    def receive_damage(self, damage):
        self.health -= damage
        if self.health <= 0:
            self.health = 0
            self.game.score += 100
            self.kill()


class Bullet(pygame.sprite.Sprite):
    def __init__(self, game, position, velocity,
                 spread, ttl, speed, damage, color, size, target_group):

        self.groups = game.all_sprites, game.bullets
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pygame.Surface((size, size))
        self.image.fill(color)
        self.rect = self.image.get_rect()

        self.position = position
        self.rect.center = self.position

        self.ttl = ttl
        self.spawn_time = pygame.time.get_ticks()
        self.speed = uniform(speed * 0.9, speed * 1.1)
        self.damage = damage
        self.velocity = velocity + Vector2(
            uniform(-spread, spread), uniform(-spread, spread))
        self.velocity = self.velocity.normalize()
        self.target_group = target_group

    def update(self):
        self.position += self.velocity * self.speed * self.game.dt
        self.rect.center = self.position

        life_time = pygame.time.get_ticks() - self.spawn_time

        if life_time > self.ttl:
            self.kill()

        if pygame.sprite.spritecollide(self, self.game.walls, False):
            self.kill()

        hits = pygame.sprite.spritecollide(self, self.target_group, False)
        if len(hits) > 0:
            hits[0].receive_damage(self.damage)
            self.kill()


class Item(pygame.sprite.Sprite):
    def __init__(self, game, position, kind):
        self.groups = game.all_sprites, game.items
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.data = Data()
        self.game = game
        self.image = self.data.healthpack_img
        self.rect = self.image.get_rect()
        self.position = position
        self.rect.topleft = position
        self.kind = kind

    def update(self):
        self.rect.top = self.position.y + math.sin(pygame.time.get_ticks() *
                                                   ITEM_HOVER_SPEED) * TILESIZE // 2
        if pygame.sprite.collide_rect(self, self.game.player):
            self.picked_by(self.game.player)

    def picked_by(self, picker):
        pass


class HealthPack(Item):
    def __init__(self, game, position):
        super().__init__(
            game,
            position,
            'HEALTHPACK'
        )
        self.image = self.data.healthpack_img

    def picked_by(self, picker):
        heal = ITEMS[self.kind]['HEAL']
        if picker.health < picker.max_health:
            picker.health = min(picker.health + heal, picker.max_health)
            self.kill()


class SpeedUp(Item):
    def __init__(self, game, position):
        super().__init__(
            game,
            position,
            'SPEEDUP'
        )
        self.image = self.data.speedup_img
        self.picker = None
        self.picker_base_speed = 0
        self.picker_max_speed = 0

    def picked_by(self, picker):

        self.picker = picker

        speed_up = ITEMS[self.kind]['SPEED']
        picker.max_speed += speed_up

        ttl = ITEMS[self.kind]['TTL']
        self.stop_working_at = pygame.time.get_ticks() + ttl
        self.rect.x = -10000000

        # TODO: investigar set_timer()

    def update(self):
        if self.picker == None:
            super().update()
            return

        now = pygame.time.get_ticks()
        if now > self.stop_working_at:
            speed_up = ITEMS[self.kind]['SPEED']
            self.picker.max_speed -= speed_up
            self.kill()
