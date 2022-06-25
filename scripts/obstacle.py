import pygame
from settings import *

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, pos, groups, player, game):
        super().__init__(groups)

        # general setup
        house_frame_1 = self.scaled_sprite(frame=1)
        house_frame_2 = self.scaled_sprite(frame=2)
        house_frame_3 = self.scaled_sprite(frame=3)
        house_frame_4 = self.scaled_sprite(frame=4)
        house_frame_5 = self.scaled_sprite(frame=5)
        house_frame_6 = self.scaled_sprite(frame=6)
        self.frames = [house_frame_1, house_frame_2, house_frame_3, house_frame_4, house_frame_5, house_frame_6]
        self.frame_index = 0
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect(topleft = pos)
        self.health = 6
        self.player = player
        self.game = game

    def scaled_sprite(self, frame):
        original_sprite = pygame.image.load(f'../graphics/other/house-{frame}.png').convert_alpha()
        scaled_width = original_sprite.get_width() * (WINDOW_WIDTH / 100)
        scaled_height = original_sprite.get_height() * (WINDOW_HEIGHT / 100)
        scaled_sprite = pygame.transform.scale(original_sprite, (scaled_width, scaled_height))
        return scaled_sprite

    # Obstacle damage function
    def take_damage(self):
        # if health is at zero or self.frame_index is at max
        if self.health == 0 or self.frame_index == 5:
            self.kill() # destroy obstacle
            self.player.sprite.hearts -= 1 # take a heart off the player
            self.game.player_death_sound.play()
        else:
            self.health -= 1
            self.frame_index += 1


    # updates sprite based on health
    def damage_state(self):
        self.image = self.frames[self.frame_index]



    def update(self):
        self.damage_state()
