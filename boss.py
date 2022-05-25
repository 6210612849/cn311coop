#from curses import COLOR_BLUE
import pygame
import random

pygame.font.init()

class Boss():
    def __init__(self, x, y, width, height, color):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.rect = (x, y, width, height)
        self.hp = 100
        self.velx = 5

        self.attack_delay = False

    def draw(self, win):
        
        font=pygame.font.Font('BitMap.ttf', 30)
        hpText = font.render(str(self.hp), True, (255, 0, 0))
        win.blit(hpText, (40, 250))

        if self.hp <= 0:
            pygame.draw.rect(win, (255, 255, 0), self.rect)
            
            
        else:

            pygame.draw.rect(win, self.color, self.rect)

    def update(self):

        if self.x <= 395 and self.x >= 5:

            self.x = self.x+self.velx
        elif self.x <= 400 and self.x >= 395:

            self.velx = -5
            self.x = self.x+self.velx
        elif self.x >= 0 and self.x <= 5:
            self.velx = 5
            self.x = self.x+self.velx
        self.rect = (self.x, self.y, self.width, self.height)
