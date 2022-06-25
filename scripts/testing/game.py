import pygame, sys
from menu import MainMenu, OptionMenu, CreditsMenu
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 800

class Game():
    def __init__(self):
        pygame.init()
        # running = True when game is on
        # playing = True when game is actually being played (in game loop)
        self.running, self.playing = True, False
        self.UP_KEY, self.DOWN_KEY, self.START_KEY, self.BACK_KEY = False, False, False, False
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.main_menu = MainMenu(self)
        self.option_menu = OptionMenu(self)
        self.credits_menu = CreditsMenu(self)
        self.curr_menu = self.main_menu

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running, self.playing = False, False
                self.curr_menu.run_display = False
            if event.type == pygame.KEYDOWN:
                if self.playing == False: # if the game is not being played
                    if event.key == pygame.K_RETURN:
                        self.START_KEY = True
                    if event.key == pygame.K_BACKSPACE:
                        self.BACK_KEY = True
                    if event.key == pygame.K_DOWN:
                        self.DOWN_KEY = True
                    if event.key == pygame.K_UP:
                        self.UP_KEY = True

    def reset_keys(self):
        self.UP_KEY, self.DOWN_KEY, self.START_KEY, self.BACK_KEY = False, False, False, False

    # draws text
    def draw_text(self, text, size, x, y):
        font = pygame.font.Font(r'C:\Users\indic\OneDrive\The Indie Project\Programming Projects\Space Invaders\graphics\font\Pixeltype.ttf', size)
        text_surface = font.render(text, True, 'White')
        text_rect = text_surface.get_rect()
        text_rect.center = (x,y)
        self.display_surface.blit(text_surface, text_rect)

    def run(self):
        while self.playing: # if game is being played
            self.check_events() # check all events
            if self.START_KEY: # if player has selected start key
                self.playing = False
            self.display_surface.fill((0,0,0))
            self.draw_text("Thanks for Playing", 50, WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2)
            pygame.display.update()
            self.reset_keys()


# g = Game()
# while g.running:
#     g.curr_menu.display_menu()
#     g.run()

if __name__ == "__main__":
    game = Game()
    while game.running:
        game.curr_menu.display_menu()
        game.run()
