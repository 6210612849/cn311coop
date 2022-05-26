from itertools import count
import socket
from _thread import *
import sys
import pickle
from player import Player
from bullet import Bullet
from boss import Boss
import pygame
from random import Random, random
from bossBullet import BossBullet
server = "172.20.10.3"
port = 8080

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))

except socket.error as e:
    str(e)

s.listen(2)
print("waiting connection")

players = [Player(150, 350, 50, 50, (255, 0, 0)),
           Player(350, 350, 50, 50, (0, 255, 0)),
           Player(250, 250, 50, 50, (255, 0, 0)), Player(70, 350, 50, 50, (255, 0, 0)), ]
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


def thread_check_create(conn,):
    global room_avalible, currentPlayer, count_max_player
    data = pickle.loads(conn.recv(2048))
    """ print("hey check room")
    print((data))
    print((data.index))
    print(type(data.index)) """
    if data.index == 6:
        room_avalible = True
        count_max_player = data.data
        print(room_avalible)
    if room_avalible:
        #print("hey check room2")
        start_new_thread(thread_client, (conn, currentPlayer,))
        currentPlayer += 1


def thread_server():
    global room_ready, players_hp
    if room_ready:
        clock = pygame.time.Clock()
        while True:
            clock.tick(60)
            boss[0].update()
            for bullet in bullets:
                if bullet.y >= 0:
                    if (bullet.x > boss[0].x and bullet.x < boss[0].x+boss[0].width) and (bullet.y > boss[0].y and bullet.y < boss[0].y+boss[0].height):
                        bullets.remove(bullet)
                        boss[0].hp -= 10
                else:
                    bullets.remove(bullet)
                bullet.update()
            r = Random()
            if(r.randrange(0, 10000) < 700):
                bossBullets.append(
                    BossBullet(boss[0].x + boss[0].height/2, boss[0].width/2))
            for bossbullet in bossBullets:
                bossbullet.update()
                if bossbullet.y >= 0 and bossbullet.y < 500:
                    if count_max_player == 4:
                        condition1 = (bossbullet.x > players[0].x and bossbullet.x < players[0].x+players[0].width) and (
                            bossbullet.y > players[0].y and bossbullet.y < players[0].y+players[0].height)
                        condition2 = (bossbullet.x > players[1].x and bossbullet.x < players[1].x+players[1].width) and (
                            bossbullet.y > players[1].y and bossbullet.y < players[1].y+players[1].height)
                        condition3 = (bossbullet.x > players[2].x and bossbullet.x < players[2].x+players[2].width) and (
                            bossbullet.y > players[2].y and bossbullet.y < players[2].y+players[2].height)
                        condition4 = (bossbullet.x > players[3].x and bossbullet.x < players[3].x+players[3].width) and (
                            bossbullet.y > players[3].y and bossbullet.y < players[3].y+players[3].height)
                        if (condition1 or condition2 or condition3 or condition4):
                            players_hp -= 1
                            bossBullets.remove(bossbullet)
                    elif count_max_player == 3:
                        condition1 = (bossbullet.x > players[0].x and bossbullet.x < players[0].x+players[0].width) and (
                            bossbullet.y > players[0].y and bossbullet.y < players[0].y+players[0].height)
                        condition2 = (bossbullet.x > players[1].x and bossbullet.x < players[1].x+players[1].width) and (
                            bossbullet.y > players[1].y and bossbullet.y < players[1].y+players[1].height)
                        condition3 = (bossbullet.x > players[2].x and bossbullet.x < players[2].x+players[2].width) and (
                            bossbullet.y > players[2].y and bossbullet.y < players[2].y+players[2].height)
                        if (condition1 or condition2 or condition3):
                            players_hp -= 1
                            bossBullets.remove(bossbullet)
                    elif count_max_player == 2:
                        condition1 = (bossbullet.x > players[0].x and bossbullet.x < players[0].x+players[0].width) and (
                            bossbullet.y > players[0].y and bossbullet.y < players[0].y+players[0].height)
                        condition2 = (bossbullet.x > players[1].x and bossbullet.x < players[1].x+players[1].width) and (
                            bossbullet.y > players[1].y and bossbullet.y < players[1].y+players[1].height)

                        if (condition1 or condition2):

                            players_hp -= 1
                            bossBullets.remove(bossbullet)
                            
                else:
                    bossBullets.remove(bossbullet)


def thread_client(conn, player):
    
    print("in thredad", player)
    conn.send(pickle.dumps("connect complete"))
    reply = ""
    count_test = 0
    while True:
        try:


            data = pickle.loads(conn.recv(2048))
            
            count_test += 1
            if data.index == 0:
                conn.send(pickle.dumps(players[player]))
            if data.index == 1:
                players[player] = data.data
                if not data:
                   
                    break
                else:
                    reply_temp = []
                    if player == 0:
                        if count_max_player == 4:
                            reply_temp.append(players[1])
                            reply_temp.append(players[2])
                            reply_temp.append(players[3])
                            reply = reply_temp
                        elif count_max_player == 3:
                            reply_temp.append(players[1])
                            reply_temp.append(players[2])

                            reply = reply_temp
                        elif count_max_player == 2:
                            reply_temp.append(players[1])
                            reply = reply_temp
                    elif player == 1:
                        if count_max_player == 4:
                            reply_temp.append(players[0])
                            reply_temp.append(players[2])
                            reply_temp.append(players[3])
                            reply = reply_temp
                        elif count_max_player == 3:
                            reply_temp.append(players[0])
                            reply_temp.append(players[2])
                            reply = reply_temp
                        elif count_max_player == 2:
                            reply_temp.append(players[0])
                            reply = reply_temp

                    elif player == 2:
                        if count_max_player == 4:
                            reply_temp.append(players[0])
                            reply_temp.append(players[1])
                            reply_temp.append(players[3])
                            reply = reply_temp
                        elif count_max_player == 3:
                            reply_temp.append(players[0])
                            reply_temp.append(players[1])
                            reply = reply_temp

                    else:
                        reply = players[0:3]
                   

                conn.sendall(pickle.dumps(reply))
            if data.index == 2:
                bullets.append(data.data)
                print("bullet", bullets)
            if data.index == 3:
                conn.sendall(pickle.dumps(bullets))
            if data.index == 4:

                conn.sendall(pickle.dumps(boss[0]))
            if data.index == 5:

                global count_player_in_room, room_ready
                print("aaeeeeee", count_player_in_room)
                if data.data == "NOTREADY":
                    print("to ready")
                    count_player_in_room += 1
                    reply = "READY"
                else:
                    print("to notready")
                    count_player_in_room -= 1
                    reply = "NOTREADY"
                if count_max_player == count_player_in_room:
                    room_ready = True
                    start_new_thread(thread_server, ())
                conn.sendall(pickle.dumps(reply))
            if data.index == 7:

                if room_ready:
                    conn.sendall(pickle.dumps(1))
                else:
                    conn.sendall(pickle.dumps(0))
            if data.index == 8:
                conn.sendall(pickle.dumps(bossBullets))
            if data.index == 9:
                conn.sendall(pickle.dumps(players_hp))
        except socket.error as e:
            print(e)
            break
    
    conn.close()


room_ready = False
room_avalible = False
currentPlayer = 0
server_status = 'start'
count_player_in_room = 0
count_max_player = 0
while True:
    conn, addr = s.accept()
    
    if room_avalible:
        start_new_thread(thread_client, (conn, currentPlayer,))
        currentPlayer += 1
    else:
        conn.send(pickle.dumps("connect complete"))
        start_new_thread(thread_check_create, (conn,))
