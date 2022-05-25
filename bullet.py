import pygame
from network import Network


class Bullet():
    def __init__(self, x, y):

        self.x = x+7.5
        self.y = y
        self.color = (0, 255, 0)
        self.width = 15
        self.height = 15

    def draw(self, win):
        bulletImg = pygame.image.load(
            r'.\bullet.png')
        bulletImg = pygame.transform.smoothscale(
            bulletImg, (self.width, self.height))
        win.blit((bulletImg), (self.x, self.y))

    def update(self):
        self.x = self.x
        self.y = self.y-10
