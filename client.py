
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
    global test 
    
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            run = False
            pygame.quit()

    """ 
    if(test == 100):
        print("test")
        pygame.quit()
        global currentState 
        currentState = state[0]
        print(currentState)
        print("-----------------------------------------------------------------------")
    else:
        test = test+1 """
    
    p.move(n)

    print('im in player run')
    redrawWindow(win, p, p2, Bullets, boss)

def preStart(p, n, clock):
    
    global playerId, getPlayerId, currentState

    data = 'N'

    while(True):

        status = n.sendReady(data)
        
        if(getPlayerId):
            print('change getPlayerId')
            playerId = status
            getPlayerId = False
            data = 'R'
            print('playerID')
            print(playerId)
            print('current state:' + currentState)
            #print(status)

        if (status == 'ready'):
            print('change state')
            currentState = state[1]
            print(status)
            print(playerId)
            break

    
        
        #print("state change to" + currentState)
        

def main():
    run = True

    n = Network()

    p = n.getP()
    clock = pygame.time.Clock()


    while run:
        clock.tick(60)

        match(currentState): 
            case 'N':
                preStart(p, n, clock)

            case 'R':
                # print('state R')
                playerRun(p, n, clock)


        


main()
