from bullet import Bullet
import pygame
from network import Network


class Player():
    def __init__(self, x, y, width, height, color):

        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.rect = (x, y, width, height)
        self.vel = 3
        self.shot_delay = False
        self.COOLDOWN_TIME_MS = 100
        self.countShotDelay = 0

        self.speed_buff_cooldown = False
        self.COOLDOWN_SPEED = 1000
        self.countSpeedtCooldown = 0

        self.GetSpeedBuff = False
        self.SpeedBuff = 0
        self.SpeedBuffLimit = 300

    def draw(self, win):
        sprites = pygame.image.load(
            r'.\ufo.png')

        win.blit(sprites, (self.x, self.y))
        if self.GetSpeedBuff:
            # print("sprite speed buff")
            windSprites = pygame.image.load(
                r'.\Wind-PNG-Images.png')
            windSprites = pygame.transform.smoothscale(windSprites, (50, 50))
            win.blit(windSprites, (450, 450))

    def move(self, n):

        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            if self.x >= 20:
                self.x -= self.vel

        if keys[pygame.K_RIGHT]:
            if self.x <= 470:
                self.x += self.vel

        if keys[pygame.K_UP]:
            if self.y >= 20:
                self.y -= self.vel

        if keys[pygame.K_DOWN]:
            if self.y <= 470:
                self.y += self.vel

        if self.countShotDelay >= self.COOLDOWN_TIME_MS:
            self.shot_delay = False
            self.countShotDelay = 0
        if keys[pygame.K_SPACE] and not self.shot_delay:
            # print("space")

            self.shot_delay = True
            bulletShooting = Bullet(self.x, self.y)
            n.sendBullet(bulletShooting)

        if self.countSpeedtCooldown >= self.COOLDOWN_SPEED:

            self.speed_buff_cooldown = False
            self.countSpeedtCooldown = 0

        if keys[pygame.K_LSHIFT] and not self.speed_buff_cooldown:
            # print("Speed buff")
            self.vel = 10
            self.GetSpeedBuff = True
            self.speed_buff_cooldown = True
        if self.GetSpeedBuff:
            if self.SpeedBuff >= self.SpeedBuffLimit:
                self.vel = 3
                self.GetSpeedBuff = False
                self.SpeedBuff = 0
            self.SpeedBuff += 1

        self.update()

    def update(self):
        self.countShotDelay += 1
        self.countSpeedtCooldown += 1
        self.rect = (self.x, self.y, self.width, self.height)
