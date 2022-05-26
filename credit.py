import pygame
import pygame.freetype
from pygame.sprite import Sprite
from pygame.rect import Rect


class creditscreen(Sprite):
    def draw(self, win):
        HowtoSprites = pygame.image.load(
            r'.\pic\credit.jpg')
        win.blit(HowtoSprites, (0, 0))
