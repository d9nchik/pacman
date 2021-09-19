import pygame.mixer

from src.enemies import Blinky, Inky, Pinky, Clyde
from src.entity import Block, Ellipse
from src.environment import generate_environment, draw_environment
from src.player import Player
from src.settings import *

pygame.mixer.init()


# TODO: add rage

class Game(object):
    # load sounds
    pacman_sound = pygame.mixer.Sound("./src/sounds/pacman_sound.ogg")
    game_over_sound = pygame.mixer.Sound("./src/sounds/game_over_sound.ogg")
    win_sound = pygame.mixer.Sound('./src/sounds/win.ogg')
    hurt = pygame.mixer.Sound('./src/sounds/hurt.wav')
    upgrade = pygame.mixer.Sound('./src/sounds/upgrade.wav')

    def __init__(self, records):
        self.records = records

        self.game_over = True
        self.win = False
        self.life = MAX_LIFE_LEVEL
        # font for score on the screen
        self.font = pygame.font.Font(None, 35)

        self.score = 0
        self.level = 1
        self.grid = generate_environment()

        self.player = Player(self.grid)
        # paths blocks
        self.empty_blocks = pygame.sprite.Group()
        self.non_empty_blocks = pygame.sprite.Group()
        self.dots_group = pygame.sprite.Group()

        for i, row in enumerate(self.grid):
            for j, item in enumerate(row):
                if item == 0:
                    self.empty_blocks.add(
                        Block(j * BLOCK_SIZE + 8, i * BLOCK_SIZE + 8, BLACK, HALF_BLOCK_SIZE + 4, HALF_BLOCK_SIZE + 4))
                else:
                    self.non_empty_blocks.add(
                        Block(j * BLOCK_SIZE + QUARTER_BLOCK_SIZE, i * BLOCK_SIZE + QUARTER_BLOCK_SIZE, BLACK,
                              HALF_BLOCK_SIZE, HALF_BLOCK_SIZE))
                    self.dots_group.add(Ellipse(j * BLOCK_SIZE + 12, i * BLOCK_SIZE + 12, WHITE, QUARTER_BLOCK_SIZE,
                                                QUARTER_BLOCK_SIZE))

        block = pygame.sprite.spritecollide(self.player, self.non_empty_blocks, False)[0]
        self.player_i = int((block.rect.y - QUARTER_BLOCK_SIZE) // BLOCK_SIZE)
        self.player_j = int((block.rect.x - QUARTER_BLOCK_SIZE) // BLOCK_SIZE)

        self.blinky = Blinky(self.grid, self.player_i, self.player_j)
        self.clyde = Clyde(self.grid, self.player_i, self.player_j)
        self.inky = Inky(self.grid, self.player_i, self.player_j)
        self.pinky = Pinky(self.grid, self.player_i, self.player_j)
        self.enemies = pygame.sprite.Group()
        self.enemies.add(self.blinky, self.clyde, self.inky, self.pinky)

    def run_logic(self):
        if not self.game_over:
            self.player.update(self.empty_blocks)
            block_hit_list = pygame.sprite.spritecollide(self.player, self.dots_group, True)
            if len(block_hit_list) > 0:
                self.pacman_sound.play()
                self.score += len(block_hit_list)
            if self.life > 1:
                block_hit_list = pygame.sprite.spritecollide(self.player, self.enemies, False)
                if len(block_hit_list) > 0:
                    self.decrease_life_level()
            else:
                block_hit_list = pygame.sprite.spritecollide(self.player, self.enemies, True)
                if len(block_hit_list) > 0:
                    self.life -= 1
                    self.player.explosion = True
                    self.game_over_sound.play()
            self.game_over = self.player.game_over

            blocks = pygame.sprite.spritecollide(self.player, self.non_empty_blocks, False)
            if len(blocks) != 0:
                self.player_i = int((blocks[0].rect.y - QUARTER_BLOCK_SIZE) // BLOCK_SIZE)
                self.player_j = int((blocks[0].rect.x - QUARTER_BLOCK_SIZE) // BLOCK_SIZE)

            self.enemies.update(self.player_i, self.player_j)
            # win effect
            if len(self.dots_group) == 0:
                self.upgrade.play()
                self.increase_level()

            if self.level == MAX_LEVEL + 1:
                self.game_over = True
                self.win = True
                self.win_sound.play()
            if self.game_over:
                self.records.add_score(self.score)

    def decrease_life_level(self):
        self.life -= 1
        self.player = Player(self.grid)
        self.hurt.play()

    def increase_level(self):
        level = self.level + 1
        score = self.score
        life = self.life
        self.__init__(self.records)
        self.level = level
        self.life = life
        self.score = score
        self.game_over = False

    def draw_game(self, screen):
        draw_environment(screen, self.grid)
        self.dots_group.draw(screen)
        self.enemies.draw(screen)
        screen.blit(self.player.image, self.player.rect)
        # Render the text for the score
        text = self.font.render("Score: {}; Level: {}: HP: {}".format(self.score, self.level, self.life), True,
                                WHITE)
        # put text on screen
        screen.blit(text, [120, 20])
