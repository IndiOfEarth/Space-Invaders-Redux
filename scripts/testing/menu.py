import pygame
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 800
SIZE = 50

class Menu():
    def __init__(self, game):
        self.game = game # a reference to the game object
        self.mid_w, self.mid_h = WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2
        self.run_display = True # tells menu to keep running until false
        self.cursor_rect = pygame.Rect(0, 0, 20, 20) # border/space aroud the cursor
        self.offset = -100 # offset for the cursor


    # draws text
    def draw_text(self, text, size, x, y):
        font = pygame.font.Font(r'C:\Users\indic\OneDrive\The Indie Project\Programming Projects\Space Invaders\graphics\font\Pixeltype.ttf', size)
        text_surface = font.render(text, True, 'White')
        text_rect = text_surface.get_rect()
        text_rect.center = (x,y)
        self.game.display_surface.blit(text_surface, text_rect)

    # draws menu select cursor
    def draw_cursor(self):
        self.draw_text('*', 15, self.cursor_rect.x, self.cursor_rect.y)

    # blits the menu to the screen
    def blit_screen(self):
        # ALT - better idea to draw everything to a surface and then blit that to screen
        pygame.display.update()
        self.game.reset_keys()

# Each class will inherit from Menu()
class MainMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.state = "Start" # Tracks the state of the cursor
        self.startx, self.starty = self.mid_w, self.mid_h + 70
        self.optionsx, self.optionsy = self.mid_w, self.mid_h + 120
        self.creditsx, self.creditsy = self.mid_w, self.mid_h + 170
        self.cursor_rect.midtop = (self.startx + self.offset, self.starty) # assign cursor position

    # displays this menu to window
    def display_menu(self):
        self.run_display = True # tells menu to keep running
        while self.run_display:
            self.game.check_events() # checks events for key input
            self.check_input() # handles input and changes menu/scene based on it
            self.game.display_surface.fill((0,0,0))
            self.draw_text('Main Menu', SIZE, WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2 -20)
            self.draw_text('Start Game', SIZE, self.startx, self.starty)
            self.draw_text('Options', SIZE, self.optionsx, self.optionsy)
            self.draw_text('Credits', SIZE, self.creditsx, self.creditsy)
            self.draw_cursor()
            self.blit_screen()

    # handles cursor movement and logic
    def move_cursor(self):
        if self.game.DOWN_KEY: # if the DOWN_KEY has been pressed (only if game.playing == False)
            if self.state == 'Start':
                self.cursor_rect.midtop = (self.optionsx + self.offset, self.optionsy)
                self.state = 'Options'
            elif self.state == 'Options':
                self.cursor_rect.midtop = (self.creditsx + self.offset, self.creditsy)
                self.state = 'Credits'
            elif self.state == 'Credits':
                self.cursor_rect.midtop = (self.startx + self.offset, self.starty)
                self.state = 'Start'
        elif self.game.UP_KEY: # if the UP_KEY has been pressed (only if game.playing == False)
            if self.state == 'Start':
                self.cursor_rect.midtop = (self.creditsx + self.offset, self.creditsy)
                self.state = 'Credits'
            elif self.state == 'Options':
                self.cursor_rect.midtop = (self.startx + self.offset, self.starty)
                self.state = 'Start'
            elif self.state == 'Credits':
                self.cursor_rect.midtop = (self.optionsx + self.offset, self.optionsy)
                self.state = 'Options'


    def check_input(self):
        self.move_cursor()
        if self.game.START_KEY:
            if self.state == "Start":
                self.game.playing = True
            elif self.state == "Options":
                self.game.curr_menu = self.game.option_menu
            elif self.state == "Credits":
                self.game.curr_menu = self.game.credits_menu
            self.run_display = False # will stop displaying this Menu

class OptionMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.state = 'Volume' # Tracks state of cursor
        self.volx, self.voly = self.mid_w, self.mid_h + 20
        self.controlsx, self.controlsy = self.mid_w, self.mid_h + 60
        self.cursor_rect.midtop = (self.volx + self.offset, self.voly)

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events() # checks for input
            self.check_input() # logic that decides what to do with input
            self.game.display_surface.fill((0,0,0))
            self.draw_text('Options', SIZE, WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2 -20)
            self.draw_text('Volume', SIZE-10, self.volx, self.voly)
            self.draw_text('Controls', SIZE-10, self.controlsx, self.controlsy)
            self.draw_cursor()
            self.blit_screen()

    def check_input(self):
        if self.game.BACK_KEY: # if player hits backspace
            self.game.curr_menu = self.game.main_menu # sets back to main menu
            self.run_display = False
        elif self.game.UP_KEY or self.game.DOWN_KEY:
            if self.state == 'Volume':
                self.state = 'Controls'
                self.cursor_rect.midtop = (self.controlsx + self.offset, self.controlsy)
            elif self.state == 'Controls':
                self.state = 'Volume'
                self.cursor_rect.midtop = (self.volx + self.offset, self.voly)
        elif self.game.START_KEY:
            # Take to volume or controls menu
            pass

class CreditsMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            if self.game.START_KEY or self.game.BACK_KEY:
                self.game.curr_menu = self.game.main_menu
                self.run_display = False
            self.game.display_surface.fill((0,0,0))
            self.draw_text('Credits', SIZE, WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2 -20)
            self.draw_text('Made by me', SIZE-10, WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2 +40)
            self.blit_screen()
