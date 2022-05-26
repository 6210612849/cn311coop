from itertools import count
import socket
from _thread import *
import sys
import pickle
from player import Player
from bullet import Bullet
from boss import Boss

server = "172.20.10.3"
port = 465

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))

except socket.error as e:
    str(e)

s.listen(2)
print("waiting connection")

players = [Player(150, 350, 50, 50, (255, 0, 0)),
           Player(350, 350, 50, 50, (0, 255, 0))]
count_player = 0
bullets = []
bossBullets = []
players_hp = 100
boss = [Boss(150, 0, 100, 100, (255, 0, 0)), ]


def read_pos(str):
    str = str.split(",")
    return int(str[0]), int(str[1])


def make_pos(tup):
    return str(tup[0])+","+str(tup[1])


def thread_client(conn, player):
    # print("thred first", pickle.dumps(players[player]))
    conn.send(pickle.dumps(players[player]))

    # print("connect conn")
    reply = ""
    count_test = 0
    while True:
        try:
            # data = pickle.loads(conn.recv(2048))
            # players[player] = data

            # if not data:
            #     print("disconnected no data")
            #     break
            # else:
            #     if player == 1:
            #         reply = players[0]
            #     else:
            #         reply = players[1]
            #     print("recieved:", reply)
            # conn.sendall(pickle.dumps(reply))

            data = pickle.loads(conn.recv(2048))
            # print("test", count_test)
            count_test += 1
            if data.index == 1:
                players[player] = data.data
                # print("newtype old", players[player])

                if not data:
                    # print("disconnected no data")
                    break
                else:
                    if player == 0:
                        reply = players[1]
                    else:
                        reply = players[0]
                    # print("recieved:", reply)

                conn.sendall(pickle.dumps(reply))
            if data.index == 2:
                bullets.append(data.data)
            if data.index == 3:
                for bullet in bullets:
                    if bullet.y >= 0:
                        bullet.update()
                        if (boss[0].hp <= 0) and (bullet.x > boss[0].x and bullet.x < boss[0].x+boss[0].width) and (bullet.y > boss[0].y and bullet.y < boss[0].y+boss[0].height):
                            print("hitboss after ded")
                            bullets.remove(bullet)
                            print('i ll send sometrhing')
                        else:
                            if (bullet.x > boss[0].x and bullet.x < boss[0].x+boss[0].width) and (bullet.y > boss[0].y and bullet.y < boss[0].y+boss[0].height):
                                print("hit", bullet.x)
                                bullets.remove(bullet)
                                boss[0].hp -= 10
                                print("hit", boss[0].hp)
                
                    else:
                        bullets.remove(bullet)

                conn.sendall(pickle.dumps(bullets))
            if data.index == 4:
                boss[0].update()
                conn.sendall(pickle.dumps(boss[0]))
            if data.index == 5:

                global count_player

                if not data:
                    # print("disconnected no data")
                    break
                status = data.data
                # it will give client a id when they access this code in first time
                if (status == 'N'):
                    if(count_player != 3):
                        count_player += 1
                        reply = str(count_player)
                        print('new count_player' + str(count_player))
                else:
                    #reply = 'wait'
                    if(count_player == 2):
                        reply = 'R'

                conn.sendall(pickle.dumps(reply))

            #getBossBullet
            if data.index == 7:
                global players_hp
                for bossbullet in bossBullets:
                    
                    
                    if bossbullet.y >= 0 and bossbullet.y < 500:
                        bossbullet.update()
                        condition1 = (bossbullet.x > players[0].x and bossbullet.x < players[0].x+players[0].width) and (bossbullet.y > players[0].y and bossbullet.y < players[0].y+players[0].height)
                        condition2 = (bossbullet.x > players[1].x and bossbullet.x < players[1].x+players[1].width) and (bossbullet.y > players[1].y and bossbullet.y < players[1].y+players[1].height)
                        
                        #print(bossbullet.x, bossbullet.y)
                        if (condition1 or condition2):

                            #bossBullets.remove(bullet)
                            players_hp -= 1
                            bossBullets.remove(bossbullet)
                            print("hit: ", players_hp)
                            
                            #players[i].hp = players_hp
                    
                    else:
                        bossBullets.remove(bossbullet)
                conn.sendall(pickle.dumps(bossBullets))

            #send bossbullet
            if data.index == 8:
                print(data.data)
                bossBullets.append(data.data)

            if data.index == 9:
                conn.sendall(pickle.dumps(players_hp))
            
        
        except socket.error as e:
            print(e)
            break
    # print("lost connection")
    conn.close()


currentPlayer = 0
while True:
    conn, addr = s.accept()
    #print("connected", addr)
    #print("connected", conn)
    start_new_thread(thread_client, (conn, currentPlayer,))
    currentPlayer += 1

#def getHit(p, )