import pygame
import numpy as np
from settings import *
from projectiles import Projectile

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        # setup
        self.image = self.scaled_sprite()
        self.orig_image = self.image # stores normal image surface
        self.damage_image = self.reshade(self.image)
        self.frames = [self.orig_image, self.damage_image]
        self.animation_index = 0
        self.animation_speed = 5

        self.rect = self.image.get_rect(midbottom = (WINDOW_WIDTH/2, WINDOW_HEIGHT-20))
        self.direction = pygame.math.Vector2() # stores a direction (normalized vector)
        self.speed = 350
        self.pos = pygame.math.Vector2(self.rect.topleft)
        self.score = 0
        self.hearts = 3 # player's initial amount of hearts
        self.damaged = False
        self.alive = True

        # For rotation
        self.angle_change = 0

        # projectiles
        self.projectiles = pygame.sprite.Group()
        self.can_shoot = True
        # For bullet cooldown bar
        # 1. When player shoots, cooldown_bar_length = self.recharge_time - (pygame.time.get_ticks() - self.shoot_time)
        # so it becomes length of whole bar
        # 2. cooldown_bar_length will continue to get smaller until it reaches 0
        self.recharge_time = 1400
        self.shoot_time = 0
        self.recharge_time_elapsed = 0 # The thing that changes: pygame.get_ticks() - self.shoot_time
        self.cooldown_bar_length = 100 # in pixels
        self.cooldown_bar_ratio = self.recharge_time / self.cooldown_bar_length


        # sounds
        self.player_shoot_sound = pygame.mixer.Sound('../sounds/player_shoot.wav')
        self.player_shoot_sound.set_volume(0.3)

    def scaled_sprite(self):
        original_sprite = pygame.image.load("../graphics/player/rocket_1.png").convert_alpha()
        # make the sprite width and height 1/10 of the screen size
        scaled_width = original_sprite.get_width() * (WINDOW_WIDTH/100)
        scaled_height = original_sprite.get_height() * (WINDOW_HEIGHT/100)
        scaled_sprite = pygame.transform.scale(original_sprite, (scaled_width, scaled_height))
        return scaled_sprite

    def reshade(self, surface):
        # surface = the existing pygame.Surface to be reddened. Function returns a new surface
        # 1. Make a red shade with transparency
        redshade = pygame.Surface(surface.get_rect().size).convert_alpha()
        redshade.fill((255,0,0, 100)) # red with alpha

        # 2. Merge the alpha channel of the original surface onto the redshade - np.minimum keeps minimum values (most transparent) in each pixel
        # array_alpha is basically same thing as pixels_alpha (this one is faster as no copying)
        alpha_basemask = pygame.surfarray.array_alpha(surface)
        alpha_redmask = pygame.surfarray.pixels_alpha(redshade) # Makes changes to pixels in the surface (so redshade)
        np.minimum(alpha_basemask, alpha_redmask, out=alpha_redmask)

        # 3. delete the alpha_redmask to allow blit of redshade
        del alpha_redmask

        # 4. reddening a copy of original image
        redsurf = surface.copy()
        redsurf.blit(redshade, (0,0))

        return redsurf

    # updates direction vector
    def input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT]:
            self.direction.x = 1
            self.angle_change = -45
        elif keys[pygame.K_LEFT]:
            self.direction.x = -1
            self.angle_change = 45
        else:
            self.direction.x = 0
            self.angle_change = 0
        if keys[pygame.K_SPACE] and self.can_shoot:
            self.shoot_projectile()
            self.can_shoot = False
            self.shoot_time = pygame.time.get_ticks()
            self.player_shoot_sound.play()

    # bounds for player
    def screen_constraint(self):
        if self.rect.right > WINDOW_WIDTH:
            self.rect.right = WINDOW_WIDTH
            self.pos.x = self.rect.x
        elif self.rect.left < 0:
            self.rect.left = 0
            self.pos.x = self.rect.x # passes self.pos into self.rect, otherwise it sticks for 2 ticks

    # Creates a Projectile() and adds to group when input received
    def shoot_projectile(self):
        self.projectiles.add(Projectile(pos=self.rect.center, size=self.image.get_width()))

    # Stops spam shooting
    def projectile_timer(self):
        self.recharge_time_elapsed = pygame.time.get_ticks() - self.shoot_time
        if self.recharge_time_elapsed >= self.recharge_time:
            self.can_shoot = True

    def player_death_check(self):
        if self.hearts == 0:
            self.alive = False
        else:
            pass

    # Resets all class attributes
    def reset(self):
        # setup
        self.image = self.scaled_sprite()
        self.orig_image = self.image # stores normal image surface
        self.damage_image = self.reshade(self.image)
        self.frames = [self.orig_image, self.damage_image]
        self.animation_index = 0
        self.animation_speed = 5

        self.rect = self.image.get_rect(midbottom = (WINDOW_WIDTH/2, WINDOW_HEIGHT-20))
        self.direction = pygame.math.Vector2() # stores a direction (normalized vector)
        self.speed = 350
        self.pos = pygame.math.Vector2(self.rect.topleft)
        self.score = 0
        self.hearts = 3 # player's initial amount of hearts
        self.damaged = False
        self.alive = True

        # For rotation
        self.angle_change = 0

        # projectiles
        self.projectiles = pygame.sprite.Group()
        self.can_shoot = True
        # For bullet cooldown bar
        # 1. When player shoots, cooldown_bar_length = self.recharge_time - (pygame.time.get_ticks() - self.shoot_time)
        # so it becomes length of whole bar
        # 2. cooldown_bar_length will continue to get smaller until it reaches 0
        self.recharge_time = 1400
        self.shoot_time = 0
        self.recharge_time_elapsed = 0 # The thing that changes: pygame.get_ticks() - self.shoot_time
        self.cooldown_bar_length = 100 # in pixels
        self.cooldown_bar_ratio = self.recharge_time / self.cooldown_bar_length

    # update player every frame
    def update(self, dt):

        self.input()
        # Cycles animation only if player is damaged
        if self.damaged:
            self.animation_index += self.animation_speed * dt
            if self.animation_index >= len(self.frames):
                self.animation_index = 0
            sprite_surface = self.frames[int(self.animation_index)]
        else:
            sprite_surface = self.orig_image
            self.projectile_timer() # only do projectile timer stuff if player is not damaged

        self.image = pygame.transform.rotozoom(sprite_surface, self.angle_change, 1) # updates angle and self.image
        # self.image = pygame.transform.rotozoom(self.orig_image, self.angle_change, 1) # updates angle and self.image
        self.rect = self.image.get_rect(midbottom=self.rect.midbottom) # update self.rect

        self.pos.x += self.direction.x * self.speed * dt
        self.rect.x = round(self.pos.x)
        self.screen_constraint()
        self.player_death_check()
