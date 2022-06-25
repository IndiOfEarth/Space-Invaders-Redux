import pygame, time
from settings import *
from enemy import Enemy

# Parent class
class Menu():
    def __init__(self, game):
        self.game = game # a reference to the Game object
        self.mid_w, self.mid_h = WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2
        self.run_display = True # tells menu to keep running until false
        self.cursor_rect = pygame.Rect(0, 0, 20, 20) # border/space around the cursor
        self.offset = -100

    # draw_text done using Game()'s function

    # draws menu select cursor
    def draw_cursor(self):
        self.game.draw_text('*', 15, self.cursor_rect.x, self.cursor_rect.y)

    # blits the menu to the screen
    def blit_screen(self):
        pygame.display.update()
        self.game.reset_keys()

class MainMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.state = "Start"
        self.startx, self.starty = self.mid_w, self.mid_h + 70
        self.optionsx, self.optionsy = self.mid_w, self.mid_h + 120
        self.cursor_rect.midtop = (self.startx + self.offset, self.starty)


    # displays this menu to window
    def display_menu(self):
        self.run_display = True
        while self.run_display:

            self.game.check_events() # check events for key input
            self.check_input()
            self.game.display_surface.blit(self.game.bg, (0,0))
            self.game.draw_text('SPACE INVADERS PROJECT', MENU_FONT_SIZE + 30, WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2 -20)
            self.game.draw_text('Start Game', MENU_FONT_SIZE, self.startx, self.starty)
            self.game.draw_text('Options', MENU_FONT_SIZE, self.optionsx, self.optionsy)
            self.game.draw_text('Made by Indi Caburian 2022. The Indie Project.', MENU_FONT_SIZE-20, WINDOW_WIDTH / 2, WINDOW_HEIGHT - 20)

            self.draw_cursor()
            self.blit_screen()

    # handles cursor movement and logic
    def move_cursor(self):
        if self.game.DOWN_KEY: # if down_key is pressed
            if self.state == "Start":
                self.cursor_rect.midtop = (self.optionsx + self.offset, self.optionsy)
                self.state = "Options"
            elif self.state == "Options":
                self.cursor_rect.midtop = (self.startx + self.offset, self.starty)
                self.state = "Start"
        elif self.game.UP_KEY: # if up_key is pressed
            if self.state == "Start":
                self.cursor_rect.midtop = (self.optionsx + self.offset, self.optionsy)
                self.state = "Options"
            elif self.state == "Options":
                self.cursor_rect.midtop = (self.startx + self.offset, self.starty)
                self.state = "Start"

    # handles the input
    def check_input(self):
        self.move_cursor()
        if self.game.START_KEY: # if the start key has been pressed and state has changed
            if self.state == "Start":
                self.game.playing = True
                self.game.player.sprite.alive = True
            elif self.state == "Options":
                self.game.curr_menu = self.game.option_menu
            self.run_display = False # this display will no longer run

class OptionMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.state = "Options"

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            self.check_input()
            self.game.display_surface.blit(self.game.bg, (0,0))
            self.game.draw_text("This is an options menu.", MENU_FONT_SIZE, WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2)

            self.draw_cursor()
            self.blit_screen()

    def check_input(self):
        if self.game.BACK_KEY: # if player hits backspace
            self.game.curr_menu = self.game.main_menu # sets back to main menu
            self.run_display = False
