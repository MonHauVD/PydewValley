import pygame
import sys
from settings import *
from level import Level
from menu_start_game import Game


class Game_old:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption('Pydew Valley - Nhom 8')
        self.clock = pygame.time.Clock()
        self.level = Level()

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            dt = self.clock.tick() / 1000
            self.level.run(dt)
            pygame.display.update()

if __name__ == '__main__':
	game = Game()
	game.main_menu()
     
# if __name__ == '__main__':
#     game = Game_old()
#     game.run()
