import pygame

from src.game_window import GameWindow
from src.settings import SCREEN_WIDTH, SCREEN_HEIGHT

if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("PACMAN - FOR LIFE EDITION")
    done = False
    clock = pygame.time.Clock()
    game = GameWindow(screen)

    while not done:
        done = game.process_events()
        game.run_logic()
        game.display_frame()
        clock.tick(30)
    pygame.quit()
