
from pickle import FALSE
from bullet import Bullet
import pygame
from network import Network
from player import Player
width = 500
height = 500
state = ['N', 'R', 'W']
currentState = state[0]
playerId = ''
getPlayerId = True
run =True
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Client")
COOLDOWN_TIME_MS = 1000
clientNumber = 0
test = 1


def read_pos(str):
    str = str.split(",")
    return int(str[0]), int(str[1])


def make_pos(tup):
    return str(tup[0])+","+str(tup[1])


def redrawWindow(win, player, player2, Bullets, Boss):
    #print('call redrawWindow')
    win.fill((255, 255, 255))
    
    player.draw(win)
    player2.draw(win)
    for bullet in Bullets:
        if bullet:
            bullet.draw(win)
    Boss.draw(win)
    pygame.display.update()

def playerRun(p, n, clock):
    p2 = n.send(p)
    Bullets = n.getBullet()
    boss = n.getBoss()
    global test, run 
    
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            run = False
            pygame.quit()
    
    p.move(n)

    redrawWindow(win, p, p2, Bullets, boss)

def preStart(n):
    
    
    global playerId, currentState
    print(currentState)

    status = n.sendReady(currentState)

    if(currentState == 'N'):
        playerId = status
        currentState = state[2]
        print('playerID')
        print(playerId)
        print('current state:' + currentState)
    
        #print("state change to" + currentState)
def waitForStart(n):
    global playerId, currentState
    
    prevState = currentState
    status = n.sendReady(currentState)
    if (status == 'R' and prevState == 'W'):
        print('change state to R')
        currentState = state[1]

        print('playerId:'+ playerId)


def main():
    #run = True

    n = Network()

    p = n.getP()
    clock = pygame.time.Clock()


    while run:
        clock.tick(60)

        match(currentState): 
            case 'N':
                preStart(n)

            case 'W':
                waitForStart(n)

            case 'R':
                # print('state R')
                playerRun(p, n, clock)


        


main()
