import pygame

from src.entity import Entity
from src.settings import *


class Player(pygame.sprite.Sprite, Entity):
    change_x = 0
    change_y = BLOCK_SIZE
    explosion = False
    game_over = False

    def __init__(self, grid):
        pygame.sprite.Sprite.__init__(self)

        Entity.__init__(self, grid)
        self.image = pygame.image.load("./src/sprites/player.png").convert()
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.topleft = self.get_random_start_position()


    def update(self, empty_blocks):
        if not self.explosion:
            if self.rect.right < 0:
                self.rect.left = SCREEN_WIDTH
            elif self.rect.left > SCREEN_WIDTH:
                self.rect.right = 0
            if self.rect.bottom < 0:
                self.rect.top = SCREEN_HEIGHT
            elif self.rect.top > SCREEN_HEIGHT:
                self.rect.bottom = 0
            self.rect.x += self.change_x
            self.rect.y += self.change_y

            # This will stop user from moving through walls
            if len(pygame.sprite.spritecollide(self, empty_blocks, False)) > 0:
                self.rect.centerx -= self.change_x
                self.rect.centery -= self.change_y
                self.change_x = 0
                self.change_y = 0
        else:
            self.game_over = True

    def move_right(self):
        self.change_x = BLOCK_SIZE

    def move_left(self):
        self.change_x = -BLOCK_SIZE

    def move_up(self):
        self.change_y = -BLOCK_SIZE

    def move_down(self):
        self.change_y = BLOCK_SIZE

    def stop_move_horizontal(self):
        self.change_x = 0

    def stop_move_vertical(self):
        self.change_y = 0
