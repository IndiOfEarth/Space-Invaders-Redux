import pygame
from settings import *

class Projectile(pygame.sprite.Sprite):
    def __init__(self, pos, size):
        super().__init__()

        # general setup
        self.image = self.scaled_sprite(size)
        self.rect = self.image.get_rect(midbottom = pos)
        self.pos = pygame.math.Vector2(self.rect.topleft)
        self.speed = 300

    def scaled_sprite(self, size):
        original_image = pygame.image.load('../graphics/other/player_projectile.png').convert_alpha()
        scaled_size = size // 2
        scaled_sprite = pygame.transform.scale(original_image, (scaled_size, scaled_size))
        return scaled_sprite

    def update(self, dt):
        # movement
        self.pos.y -= self.speed * dt
        self.rect.y = round(self.pos.y)
        if self.rect.bottom <= -100:
            self.kill()


class EnemyProjectile(pygame.sprite.Sprite):
    def __init__(self, enemy_type, size, pos):
        super().__init__()
        # enemy_type = color of enemy that projectile is bound to
        # pos will actually be the Player's position
        # size will be enemy size

        self.type = enemy_type
        self.image = self.scaled_sprite(size)
        self.rect = self.image.get_rect(midbottom = pos)

        self.pos = pygame.math.Vector2(self.rect.topleft)
        self.speed = 300


    def scaled_sprite(self, size):
        original_image = pygame.image.load(f'../graphics/other/{self.type}_projectile.png').convert_alpha()
        scaled_size = size // 2
        scaled_sprite = pygame.transform.scale(original_image, (scaled_size, scaled_size))
        return scaled_sprite

    def update(self, dt):
        # Movement
        self.pos.y += self.speed * dt
        self.rect.y = self.pos.y
        if self.rect.bottom >= WINDOW_HEIGHT + 100:
            self.kill()
