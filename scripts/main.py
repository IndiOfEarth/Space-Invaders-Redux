import pygame, sys, time
import random
import numpy
from settings import *
from player import Player
from enemy import Enemy, UFO
from projectiles import Projectile, EnemyProjectile
from obstacle import Obstacle
from menus import Menu, MainMenu, OptionMenu


# Main game class
class Game():
    def __init__(self):
        # general setup
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.display_name = pygame.display.set_caption(WINDOW_TITLE)
        self.running, self.playing = True, False
        self.UP_KEY, self.DOWN_KEY, self.START_KEY, self.BACK_KEY = False, False, False, False
        self.main_menu = MainMenu(self)
        self.option_menu = OptionMenu(self)
        self.curr_menu = self.main_menu

        # background
        self.bg = self.create_bg()

        # groups
        self.all_sprites = pygame.sprite.Group()
        self.player = pygame.sprite.GroupSingle()
        self.enemy_sprites = pygame.sprite.Group()
        self.obstacle_sprites = pygame.sprite.Group()
        self.enemy_projectile_sprites = pygame.sprite.Group()
        self.ufo = pygame.sprite.GroupSingle()

        # sprite setup
        self.player.add(Player())
        self.ufo.add(UFO(pos=(-10,100)))
        # self.spawn_enemies(rows=5, columns=5) # spawns all enemies
        # self.spawn_obstacles()

        # UI
        self.font = pygame.font.Font('../graphics/font/Pixeltype.ttf', WINDOW_WIDTH//20)
        self.health_text = self.font.render('Health', False, 'White')
        self.recharge_text = self.font.render('Recharge', False, 'White')
        self.heart_surf = pygame.image.load('../graphics/other/heart.png').convert_alpha()


        # other
        self.enemy_direction = 1
        self.enemy_y_change = 0
        self.enemy_death_sound = pygame.mixer.Sound('../sounds/enemy_death.wav')
        self.enemy_death_sound.set_volume(0.1)
        self.enemy_shoot_sound = pygame.mixer.Sound('../sounds/alien_shoot.wav')
        self.enemy_shoot_sound.set_volume(0.2)
        self.player_death_sound = pygame.mixer.Sound('../sounds/player_death.wav')
        self.player_death_sound.set_volume(0.1)
        self.enemy_shoot_speed = 1800
        self.ufo_active = False
        self.enemy_shoot_timer = pygame.USEREVENT + 1
        self.ufo_active_timer = pygame.USEREVENT + 2
        # For damage
        self.player_damage_active = 0
        self.player_damage_time = 3000

    # event loop
    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running, self.playing = False, False
                self.curr_menu.run_display = False
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if self.playing == False: # only check these inputs when game is not being played
                    self.enemy_shoot_sound.play()
                    if event.key == pygame.K_RETURN:
                        self.START_KEY = True
                    if event.key == pygame.K_BACKSPACE:
                        self.BACK_KEY = True
                    if event.key == pygame.K_DOWN:
                        self.DOWN_KEY = True
                    if event.key == pygame.K_UP:
                        self.UP_KEY = True
            if self.playing:
                if event.type == self.enemy_shoot_timer:
                    self.enemy_shoot()
                if event.type == self.ufo_active_timer:
                    print("UFO ACTIVE")
                    # increase enemy speed and shooting speed
                    self.enemy_shoot_speed -= 200
                    all_enemies = self.enemy_sprites.sprites()
                    for enemy in all_enemies:
                        enemy.movement_speed += 10
                    self.ufo.sprite.pos.x = -10 # reset ufo position to x=50
                    self.ufo_active = True

    # Continually reseting after each loop
    def reset_keys(self):
        self.UP_KEY, self.DOWN_KEY, self.START_KEY, self.BACK_KEY = False, False, False, False

    def draw_text(self, text, size, x, y):
        text_font = pygame.font.Font('../graphics/font/Pixeltype.ttf', size)
        text_surface = text_font.render(text, True, 'White')
        text_rect = text_surface.get_rect()
        text_rect.center = (x,y)
        self.display_surface.blit(text_surface, text_rect)

    def create_bg(self):
        original_bg = pygame.image.load('../graphics/other/Star-Background.png')
        scale_factor = WINDOW_HEIGHT / original_bg.get_height()
        scaled_width = original_bg.get_width() * scale_factor
        scaled_height = original_bg.get_height() * scale_factor
        scaled_bg = pygame.transform.scale(original_bg, (scaled_width, scaled_height))
        return scaled_bg

    def display_ui(self):
        # TEXT
        health_text_pos = pygame.math.Vector2((5,10))
        recharge_text_pos = pygame.math.Vector2((500,10))
        self.display_surface.blit(self.health_text, health_text_pos)
        self.display_surface.blit(self.recharge_text, recharge_text_pos)

        # HEARTS
        self.scaled_heart_surf = pygame.transform.scale(self.heart_surf, (WINDOW_WIDTH/30, WINDOW_WIDTH/30))
        for i in range(self.player.sprite.hearts):
            x = 100 + (i * (self.heart_surf.get_width() + 30))
            self.display_surface.blit(self.scaled_heart_surf, (x, 5))

        # PROJECTILE RECHARGE BAR

        # If damaged and can't shoot, then bar is red
        if (self.player.sprite.can_shoot == False) and (self.player.sprite.damaged == True):
            pygame.draw.rect(self.display_surface, (255,0,0), (650, 10, self.player.sprite.recharge_time / self.player.sprite.cooldown_bar_ratio, 25))
        elif self.player.sprite.can_shoot == False:
            pygame.draw.rect(self.display_surface, (0,255,0), (650, 10, self.player.sprite.recharge_time_elapsed / self.player.sprite.cooldown_bar_ratio, 25)) # draws a rectangle
        else: # bar is full if player hasn't shot (self.can_shoot = True)
            pygame.draw.rect(self.display_surface, (0,255,0), (650, 10, self.player.sprite.recharge_time / self.player.sprite.cooldown_bar_ratio, 25))

    def spawn_enemies(self, rows, columns, x_distance=80, y_distance=60, x_offset=70, y_offset=80):
        # will spawn enemies once self.enemy_sprites group is empty (beginning of round and when player player kills all)
        # will also increase self.round
        for row_index, row in enumerate(range(rows)):
            for col_index, col in enumerate(range(columns)):
                pos_x, pos_y = col_index * x_distance + x_offset, row_index * y_distance + y_offset
                if 0 <= row_index <= 1: Enemy(type='blue', pos=(pos_x, pos_y), groups=[self.all_sprites, self.enemy_sprites])
                elif 2 <= row_index <= 3: Enemy(type='red', pos=(pos_x,pos_y), groups=[self.all_sprites, self.enemy_sprites])
                else: Enemy(type='purple', pos=(pos_x,pos_y), groups=[self.enemy_sprites])

    def spawn_obstacles(self, x_distance=WINDOW_WIDTH/3, x_offset=WINDOW_WIDTH/12):
        for i in range(3):
            pos_x, pos_y = i * x_distance + x_offset, WINDOW_HEIGHT*0.7
            Obstacle(pos=(pos_x, pos_y), groups=[self.all_sprites, self.obstacle_sprites], player=self.player, game=self)

    def alien_position_check(self):
        # cycle through every alien
        # if any of them is too far to the right/left, change the direction of all enemy_sprites

        self.enemy_y_change = 0 # resets enemy_y_change so doesn't constantly move down once changed
        all_enemies = self.enemy_sprites.sprites() # Gets access to all sprites in a group
        for enemy in all_enemies:
            if enemy.rect.right >= WINDOW_WIDTH:
                self.enemy_direction = -1
                self.enemy_y_change = 10
            elif enemy.rect.left <= 0:
                self.enemy_direction = 1
                self.enemy_y_change = 10

    def projectile_collision_check(self):
        for projectile in self.player.sprite.projectiles:
            # returns a list of collided sprites
            collided_sprites = pygame.sprite.spritecollide(projectile, self.enemy_sprites, False)
            if collided_sprites:
                for sprite in collided_sprites:
                    sprite.kill()
                    self.player.sprite.score += 1# increase player score
                    print(f"Score: {self.player.sprite.score}")
                    self.enemy_death_sound.play()
                projectile.kill()

    def enemy_shoot(self):
        # get random enemy from group
        random_enemy = random.choice(self.enemy_sprites.sprites())
        enemy_projectile = EnemyProjectile(enemy_type=random_enemy.type, size=random_enemy.image.get_width(), pos=random_enemy.rect.center)
        self.enemy_projectile_sprites.add(enemy_projectile)
        self.enemy_shoot_sound.play()

    def enemy_projectile_collision_check(self):
        # Checks every projectile in the enemy_projectile_sprites group and adds that projectile to list
        # if it has collided with player
        player_hit = pygame.sprite.spritecollide(self.player.sprite, self.enemy_projectile_sprites, False)
        # If player has collided with any enemy projectiles
        if player_hit:
            for projectile in player_hit:
                projectile.kill() # delete that projectile from the group and list
                self.player_death_sound.play()
                self.player.sprite.hearts -= 1 # decrease life by one
                self.player.sprite.damaged = True
                self.player.sprite.can_shoot = False # *******************************stops player shooting
                self.player_damage_active = pygame.time.get_ticks()
                print(f"Player hearts: {self.player.sprite.hearts}")
                print("Player hit") # Kill the player


        # Checks every single obstacle sprite in group
        for obstacle in self.obstacle_sprites:
            # list of any enemy_projectiles that have collided with obstacles
            collided_sprites = pygame.sprite.spritecollide(obstacle, self.enemy_projectile_sprites, False)
            if collided_sprites:
                for sprite in collided_sprites: # for each enemy projectile sprite that collided with obstacle
                    sprite.kill() # destroy it
                obstacle.take_damage() # obstacle takes damage (changes sprite)

    # Handles player.damaged state
    def player_damage_timer(self):

        if self.player.sprite.damaged:
            # Player damage animation stays for 3 seconds
            if (pygame.time.get_ticks() - self.player_damage_active) <= self.player_damage_time:
                self.player.sprite.damaged = True
            else:
                self.player.sprite.damaged = False
                self.player.sprite.can_shoot = True #**********************************************

    # Checks if all enemies are dead
    def enemies_dead_check(self):
        if not self.enemy_sprites:
            # game is over
            self.playing = False
            self.obstacle_sprites.empty()

    # Resets some game attributes
    def reset(self):
        self.enemy_direction = 1
        self.enemy_y_change = 0
        self.enemy_shoot_speed = 1800
        self.ufo_active = False
        self.player_damage_active = 0
        self.player_damage_time = 3000
        self.player.sprite.reset() # reset player attributes
        self.enemy_sprites.empty()
        self.obstacle_sprites.empty()

    def run(self):

        # Spawn/Reset everything when entering loop
        print("Spawned entities")
        self.reset() # reset game attributes and groups
        self.spawn_enemies(rows=5, columns=5)
        self.spawn_obstacles()

        # Custom Events
        pygame.time.set_timer(self.enemy_shoot_timer, self.enemy_shoot_speed)
        pygame.time.set_timer(self.ufo_active_timer, random.randint(5000, 10000))
        # pygame.time.set_timer(self.ufo_active_timer, random.randint(5000, 10000))

        previous_time = time.time() # for deltatime
        while self.playing:
            # deltatime
            dt = time.time() - previous_time
            previous_time = time.time()

            self.check_events() # event loop checks
            if self.START_KEY:
                self.playing = False # resets back to False

            self.alien_position_check() # checks postiions of enemies on screen
            self.projectile_collision_check() # checks projectile collisions
            self.enemy_projectile_collision_check()
            self.player_damage_timer()
            self.enemies_dead_check()

            # display/draw stuff
            self.display_surface.blit(self.bg, (0,0))
            self.player.update(dt)
            self.enemy_sprites.update(dt, self.enemy_direction, self.enemy_y_change)
            self.player.sprite.projectiles.update(dt)
            self.obstacle_sprites.update()
            self.enemy_projectile_sprites.update(dt)

            self.player.draw(self.display_surface)
            self.enemy_sprites.draw(self.display_surface)
            self.player.sprite.projectiles.draw(self.display_surface)
            self.obstacle_sprites.draw(self.display_surface)
            self.enemy_projectile_sprites.draw(self.display_surface)
            self.display_ui() # needs to be rendered after/ontop of everything else

            # If UFO is active (every 15 seconds by event loop)
            # Make it update and draw
            if self.ufo_active:
                self.ufo.update(dt, 1)
                self.ufo.draw(self.display_surface)
                # if ufo goes off screen, set ufo_active to false
                if self.ufo.sprite.rect.right > WINDOW_WIDTH:
                    print("UFO set to False")
                    self.ufo_active = False

            # CHECK IF PLAYER DEAD
            if self.player.sprite.alive == False: # if Player is dead
                self.playing = False # Set playing=false
                # empty all groups
                self.enemy_sprites.empty()
                self.obstacle_sprites.empty()


            # update/render window
            pygame.display.update()
            self.reset_keys()



if __name__ == "__main__":
    game = Game()
    while game.running:
        print("Beginning of loop")
        game.curr_menu.display_menu() # display a menu
        game.run() # if playing then play game
