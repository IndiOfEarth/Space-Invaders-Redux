import pygame
import random
from settings import *
from projectiles import EnemyProjectile

class Enemy(pygame.sprite.Sprite):
    def __init__(self, type, pos, groups):
        super().__init__(groups)

        # type = the color of alien (an integer) (1=purple, 2=red, 3=blue)
        # pos = Vector2 that will dictate position of the Enemy spawn
        # groups = groups that enemy will be added to

        # setup
        if type == "purple":
            alien_frame1 = self.scaled_sprite(type="purple", image_no=1).convert_alpha()
            alien_frame2 = self.scaled_sprite(type="purple", image_no=2).convert_alpha()
            alien_frame3= self.scaled_sprite(type="purple", image_no=3).convert_alpha()
            self.type = type
            self.frames = [alien_frame1, alien_frame2, alien_frame3]
            self.health = 1
        elif type == "red":
            alien_frame1 = self.scaled_sprite(type="red", image_no=1).convert_alpha()
            alien_frame2 = self.scaled_sprite(type="red", image_no=2).convert_alpha()
            self.type = type
            self.frames = [alien_frame1, alien_frame2]
            self.health = 2
        elif type == "blue":
            alien_frame1 = self.scaled_sprite(type="blue", image_no=1).convert_alpha()
            alien_frame2 = self.scaled_sprite(type="blue", image_no=2).convert_alpha()
            alien_frame3 = self.scaled_sprite(type="blue", image_no=3).convert_alpha()
            self.type = type
            self.frames = [alien_frame1, alien_frame2, alien_frame3]
            self.health = 3

        self.animation_index = 0
        self.animation_speed = 5
        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect(topleft = pos) # make this pos random

        # Movement stuff
        self.pos = pygame.math.Vector2(self.rect.topleft)
        self.movement_speed = 40


    def scaled_sprite(self, type, image_no):
        original_sprite = pygame.image.load(f"../graphics/enemies/alien-{type}-{image_no}.png").convert_alpha()
        scaled_width = original_sprite.get_width() * (WINDOW_WIDTH/120)
        scaled_height = original_sprite.get_height() * (WINDOW_HEIGHT/120)
        scaled_sprite = pygame.transform.scale(original_sprite, (scaled_width, scaled_height))
        return scaled_sprite

    def animation_state(self, dt):
        self.animation_index += self.animation_speed * dt
        if self.animation_index >= len(self.frames):
            self.animation_index = 0
        self.image = self.frames[int(self.animation_index)]

    def update(self, dt, x_direction, y_change):
        self.animation_state(dt)
        # Horizontal movement
        self.pos.x += x_direction * self.movement_speed * dt
        self.rect.x = self.pos.x
        # Vertical movement
        self.pos.y += y_change
        self.rect.y = self.pos.y

class UFO(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()

        # setup
        self.image = self.scaled_sprite()
        self.rect = self.image.get_rect(topleft = pos)

        self.pos = pygame.math.Vector2(self.rect.topleft)
        self.movement_speed = 200

    def scaled_sprite(self):
        original_sprite = pygame.image.load("../graphics/other/ufo.png")
        scaled_width, scaled_height = original_sprite.get_width() * (WINDOW_WIDTH/100), original_sprite.get_height() * (WINDOW_WIDTH/100)
        scaled_sprite = pygame.transform.scale(original_sprite, (scaled_width, scaled_height))
        return scaled_sprite

    def update(self, dt, x_direction):
        self.pos.x += x_direction * self.movement_speed * dt
        self.rect.x = self.pos.x
