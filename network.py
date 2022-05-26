import socket
import pickle
from command import Command


class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = "192.168.43.142"
        self.port = 8080
        self.addr = (self.server, self.port)
        self.p = self.connect()

    def getPlayer(self):
        try:
            data_command = Command(0, 0)

            self.client.send(pickle.dumps(data_command))

            return_dumps = pickle.loads(self.client.recv(2048))

            return return_dumps
        except socket.error as e:
            print(e)

    def getP(self):
        print("init p")
        return self.p

    def getBullet(self):
        try:
            data_command = Command(3, 0)
            self.client.send(pickle.dumps(data_command))

            return_dumps = pickle.loads(self.client.recv(2048))

            return return_dumps
        except socket.error as e:
            print(e)

    def getBoss(self):
        try:
            data_command = Command(4, 0)
            self.client.send(pickle.dumps(data_command))

            return_dumps = pickle.loads(self.client.recv(2048))

            return return_dumps
        except socket.error as e:
            print(e)

    def connect(self):
        try:
            self.client.connect(self.addr)
            return pickle.loads(self.client.recv(2048))
        except:
            pass

    def send(self, data):
        try:
            data_command = Command(1, data)

            self.client.send(pickle.dumps(data_command))

            return_dumps = pickle.loads(self.client.recv(2048))

            return return_dumps
        except socket.error as e:
            print(e)

    def sendBullet(self, data):
        try:
            data_command = Command(2, data)
            print("Bulleet data",  data_command)
            self.client.send(pickle.dumps(data_command))
        except socket.error as e:
            print(e)

    def sendReady(self, data):
        try:
            # command 5 for sent ready to server

            data_command = Command(5, data)

            self.client.send(pickle.dumps(data_command))

            return_dumps = pickle.loads(self.client.recv(2048))

            return return_dumps
        except socket.error as e:
            print(e)

    def createroom(self, data):
        try:
            # command 6 for createroom to server

            data_command = Command(6, data)

            self.client.send(pickle.dumps(data_command))

            return_dumps = pickle.loads(self.client.recv(2048))

            return return_dumps
        except socket.error as e:
            print(e)

    def checkroom(self,):
        try:
            # command 6 for createroom to server

            data_command = Command(7, 0)

            self.client.send(pickle.dumps(data_command))

            return_dumps = pickle.loads(self.client.recv(2048))

            return return_dumps
        except socket.error as e:
            print(e)

    def getBossBullet(self):
        try:
            # command 8 to request bullet

            data_command = Command(8, 0)

            self.client.send(pickle.dumps(data_command))

            return_dumps = pickle.loads(self.client.recv(2048))

            return return_dumps
        except socket.error as e:
            print(e)

    def getTeamHP(self):
        try:
            # command 7 to request bullet

            data_command = Command(9, 0)

            self.client.send(pickle.dumps(data_command))

            return_dumps = pickle.loads(self.client.recv(2048))

            return return_dumps
        except socket.error as e:
            print(e)
