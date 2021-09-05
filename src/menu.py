import pygame

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 576


class Menu(object):

    def __init__(self, items, font_color=(0, 0, 0), select_color=(0, 230, 0), ttf_font=None, font_size=25):
        self.state = 0
        self.font_color = font_color
        self.select_color = select_color
        self.items = items
        self.font = pygame.font.Font(ttf_font, font_size)

    def display_frame(self, screen):
        for index, item in enumerate(self.items):
            label = self.font.render(item, True, self.select_color if self.state == index else self.font_color)

            width = label.get_width()
            height = label.get_height()

            pos_x = (SCREEN_WIDTH / 2) - (width / 2)
            text_block_total_height = len(self.items) * height
            pos_y = (SCREEN_HEIGHT / 2) - (text_block_total_height / 2) + (index * height)

            screen.blit(label, (pos_x, pos_y))

    def event_handler(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                if self.state > 0:
                    self.state -= 1
            elif event.key == pygame.K_DOWN:
                if self.state < len(self.items) - 1:
                    self.state += 1
