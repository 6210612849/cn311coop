import socket
import pickle
from command import Command


class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = "172.20.10.3"
        self.port = 8080
        self.addr = (self.server, self.port)
        self.p = self.connect()

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
            #command 5 for sent ready to server
            
            data_command = Command(5, data)

            self.client.send(pickle.dumps(data_command))

            return_dumps = pickle.loads(self.client.recv(2048))

            return return_dumps
        except socket.error as e:
            print(e)

