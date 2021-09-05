import pygame

from src.game import Game

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 576

if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("PACMAN - FOR LIFE EDITION")
    done = False
    clock = pygame.time.Clock()
    game = Game()

    while not done:
        done = game.process_events()
        game.run_logic()
        game.display_frame(screen)
        clock.tick(30)
    pygame.quit()
