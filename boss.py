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

        sprite1 = pygame.image.load(r'.\pic\pacmanboss.png')
        sprite2 = pygame.image.load(r'.\pic\pacmanbossflip.png')

        font = pygame.font.Font('BitMap.ttf', 30)
        hpText = font.render(str(self.hp), True, (255, 0, 0))
        if(self.hp > 0):
            win.blit(hpText, (0, 0))

        if self.hp <= 0:
            #win.blit(sprite2, (self.x, self.y))
            #pygame.draw.rect(win, (255, 255, 0), self.rect)

            # you win message
            congratsText = font.render('congrats! :)', True, (255, 0, 0))
            win.blit(congratsText, (self.x, self.y))

        else:
            win.blit(sprite1, (self.x, self.y))
            #pygame.draw.rect(win, self.color, self.rect)

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
