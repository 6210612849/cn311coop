import pygame
import pygame.freetype
from pygame.sprite import Sprite
from pygame.rect import Rect


class WaitingScreen(Sprite):
    def draw(self, win):
        HowtoSprites = pygame.image.load(
            r'.\howto.jpg')
        win.blit(HowtoSprites, (0, 0))
