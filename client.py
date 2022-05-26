
from pickle import FALSE
from re import S
from sre_parse import State
from bullet import Bullet
import pygame
from network import Network
from player import Player
from menu import menuscreen
from howtoscreen import howtoscreen
from createscreen import CreateScreen
from waitingscreen import WaitingScreen
pygame.init()
width = 500
height = 500
state = ['N', 'R', 'W', 'HOWTO', 'CREATEROOM', 'NOTREADY', 'READY']
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
KEY_READY_TOGGLE = True
check_ready = "NOTREADY"
n = ""
p = ""


def read_pos(str):
    str = str.split(",")
    return int(str[0]), int(str[1])


def make_pos(tup):
    return str(tup[0])+","+str(tup[1])


def redrawWindow(win, player, player2, Bullets, Boss, BossBullets, teamHP):
    #print('call redrawWindow')
    win.fill((255, 255, 255))

    player.draw(win, teamHP)
    for p in player2:
        p.draw(win, teamHP)
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

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            run = False
            pygame.quit()
    teamHP = n.getTeamHP()
    p.move(n)

    redrawWindow(win, p, p2, Bullets, boss, BossBullets, teamHP)


def preStartHowto(screen_1_howto):
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


def preStartCreate(screen_1_create):
    global n

    global KEY_DOWN_COOLDOWN
    global playerId, currentState

    keys = pygame.key.get_pressed()
    click = pygame.mouse.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        elif event.type == pygame.KEYDOWN and not KEY_DOWN_COOLDOWN:
            KEY_DOWN_COOLDOWN = True
        elif event.type == pygame.MOUSEBUTTONDOWN and not KEY_DOWN_COOLDOWN:
            KEY_DOWN_COOLDOWN = True

    if keys[pygame.K_ESCAPE] and KEY_DOWN_COOLDOWN:
        currentState = state[0]
        KEY_DOWN_COOLDOWN = False
    elif keys[pygame.K_RIGHT] and KEY_DOWN_COOLDOWN:
        screen_1_create.update(1)
        KEY_DOWN_COOLDOWN = False
    elif keys[pygame.K_LEFT] and KEY_DOWN_COOLDOWN:
        screen_1_create.update(0)
        KEY_DOWN_COOLDOWN = False
    elif click[0] and KEY_DOWN_COOLDOWN:
        mousex, mousey = pygame.mouse.get_pos()
        if mousex >= 388 and mousex <= 500 and mousey >= 450 and mousey <= 472:
            number = screen_1_create.get_state() + 2
            print(number, "----")
            n = Network()
            n.createroom(number)
            currentState = state[2]
            print("creating room")

        KEY_DOWN_COOLDOWN = False

    win.fill((255, 255, 255))
    screen_1_create.draw(win)
    pygame.display.update()


def preStart(screen_1):

    global playerId, currentState

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
        elif my_state == 1:
            currentState = state[4]
        elif my_state == 2:
            global n
            n = Network()
            currentState = state[2]
        KEY_DOWN_COOLDOWN = False
    win.fill((255, 255, 255))
    screen_1.draw(win)

    pygame.display.update()


def waitForStart(n, screen_1_waiting):
    global playerId, currentState, KEY_DOWN_COOLDOWN, KEY_READY_TOGGLE, check_ready
    global p

    p = n.getPlayer()
    keys = pygame.key.get_pressed()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        if event.type == pygame.KEYDOWN and not KEY_DOWN_COOLDOWN:
            KEY_DOWN_COOLDOWN = True

    if keys[pygame.K_UP] and KEY_READY_TOGGLE and KEY_DOWN_COOLDOWN:
        KEY_DOWN_COOLDOWN = False
        KEY_READY_TOGGLE = False
        check_ready = n.sendReady(check_ready)

    if keys[pygame.K_DOWN] and not KEY_READY_TOGGLE and KEY_DOWN_COOLDOWN:
        KEY_DOWN_COOLDOWN = False
        KEY_READY_TOGGLE = True
        check_ready = n.sendReady(check_ready)
    check = n.checkroom()
    if check:
        currentState = state[1]
    win.fill((255, 255, 255))
    screen_1_waiting.draw(win)
    pygame.display.update()


def main():
    #run = True

    clock = pygame.time.Clock()
    screen_1 = menuscreen(font_size=30, text_rgb=(106, 159, 181), bg_rgb=(
        255, 255, 255),)
    screen_1_howto = howtoscreen()
    screen_1_create = CreateScreen(font_size=30, text_rgb=(106, 159, 181), bg_rgb=(
        255, 255, 255),)
    screen_1_waiting = WaitingScreen()
    while run:
        clock.tick(60)

        match(currentState):
            case 'N':
                preStart(screen_1)

            case 'W':
                waitForStart(n, screen_1_waiting)

            case 'R':
                # print('state R')
                playerRun(p, n, clock)
            case 'HOWTO':
                preStartHowto(screen_1_howto)
            case 'CREATEROOM':
                preStartCreate(screen_1_create)


main()
