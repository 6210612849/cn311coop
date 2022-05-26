
from pickle import FALSE
from random import Random, random
from bullet import Bullet
from bossBullet import BossBullet
import pygame
from network import Network
from player import Player
from menu import menuscreen
from howtoscreen import howtoscreen
import pickle
pygame.init()

width = 500
height = 500
state = ['N', 'R', 'W', 'HOWTO', ]
currentState = state[0]
playerId = ''
getPlayerId = True
run = True
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Client")
COOLDOWN_TIME_MS = 1000
clientNumber = 0
test = 1
KEY_DOWN_COOLDOWN = True


def read_pos(str):
    str = str.split(",")
    return int(str[0]), int(str[1])


def make_pos(tup):
    return str(tup[0])+","+str(tup[1])


def redrawWindow(win, player, player2, Bullets, Boss, BossBullets, teamHP):
    #print('call redrawWindow')
    win.fill((255, 255, 255))


    player.draw(win, teamHP)
    player2.draw(win, teamHP)
    for bullet in Bullets:
        if bullet:
            bullet.draw(win)
    for bossBullet in BossBullets:
        if bossBullet:
            bossBullet.draw(win)
    Boss.draw(win)
    pygame.display.update()


def playerRun(p, n, clock):
    p2 = n.send(p)
    Bullets = n.getBullet()
    BossBullets = n.getBossBullet()
    boss = n.getBoss()
    global test, run

    r = Random()
    if(r.randrange(0, 10000) < 700):
        bulletShooting = BossBullet(boss.x + boss.height/2, boss.width/2)
        n.sendBossBullet(bulletShooting)


    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            run = False
            pygame.quit()

    #data = pickle.loads(conn.recv(2048))

    teamHP = n.getTeamHP()
    p.move(n)

    redrawWindow(win, p, p2, Bullets, boss, BossBullets, teamHP)


def preStartHowto(n, screen_1_howto):
    global KEY_DOWN_COOLDOWN
    global playerId, currentState
    print(currentState)
    keys = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        if event.type == pygame.KEYDOWN and not KEY_DOWN_COOLDOWN:
            KEY_DOWN_COOLDOWN = True
    if keys[pygame.K_ESCAPE] and KEY_DOWN_COOLDOWN:
        currentState = state[0]
    win.fill((255, 255, 255))
    screen_1_howto.draw(win)
    pygame.display.update()


def preStart(n, screen_1):

    global playerId, currentState
    #print(currentState)

    global KEY_DOWN_COOLDOWN

    keys = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        if event.type == pygame.KEYDOWN and not KEY_DOWN_COOLDOWN:
            KEY_DOWN_COOLDOWN = True

    if keys[pygame.K_DOWN] and KEY_DOWN_COOLDOWN:
        screen_1.update(1)
        print("keydown")
        KEY_DOWN_COOLDOWN = False
    if keys[pygame.K_UP] and KEY_DOWN_COOLDOWN:
        screen_1.update(0)
        print("keydown")
        KEY_DOWN_COOLDOWN = False
    if keys[pygame.K_RETURN] and KEY_DOWN_COOLDOWN:
        my_state = screen_1.get_state()
        if my_state == 0:
            currentState = state[3]
        elif my_state == 2:
            status = n.sendReady(currentState)
            if(currentState == 'N'):
                playerId = status
                currentState = state[2]
                print('playerID')
                print(playerId)
                print('current state:' + currentState)
        KEY_DOWN_COOLDOWN = False
    win.fill((255, 255, 255))
    screen_1.draw(win)

    pygame.display.update()


def waitForStart(n):
    global playerId, currentState

    prevState = currentState
    status = n.sendReady(currentState)
    if (status == 'R' and prevState == 'W'):
        print('change state to R')
        currentState = state[1]

        print('playerId:' + playerId)


def main():
    #run = True

    n = Network()

    p = n.getP()
    clock = pygame.time.Clock()
    screen_1 = menuscreen(font_size=30, text_rgb=(106, 159, 181), bg_rgb=(
        255, 255, 255),)
    screen_1_howto = howtoscreen()

    while run:
        clock.tick(60)

        match(currentState):
            case 'N':
                preStart(n, screen_1)

            case 'W':
                waitForStart(n)

            case 'R':
                # print('state R')
                playerRun(p, n, clock)
            case 'HOWTO':
                preStartHowto(n, screen_1_howto)


main()
