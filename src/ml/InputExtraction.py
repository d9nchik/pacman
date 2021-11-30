import matplotlib.pyplot as plt
import numpy as np
import pygame
import torch
import torchvision.transforms as T
from PIL import Image
from pygame.surfarray import array3d

from src.settings import *

plt.ion()

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("PACMAN - FOR LIFE EDITION")
clock = pygame.time.Clock()

resize = T.Compose([T.ToPILImage(),
                    T.Resize(40, interpolation=Image.CUBIC),
                    T.ToTensor()])


def get_screen():
    # Returned screen requested by gym is 400x600x3, but is sometimes larger
    # such as 800x1200x3. Transpose it into torch order (CHW).
    screen1 = array3d(screen).transpose((2, 0, 1))
    # Cart is in the lower half, so strip off the top and bottom of the screen
    # _, screen_height, screen_width = screen1.shape
    # screen1 = screen1[:, int(screen_height * 0.4):int(screen_height * 0.8)]
    # Convert to float, rescale, convert to torch tensor
    # (this doesn't require a copy)
    screen1 = np.ascontiguousarray(screen1, dtype=np.float32) / 255
    screen1 = torch.from_numpy(screen1)
    # Resize, and add a batch dimension (BCHW)
    return resize(screen1).unsqueeze(0)
