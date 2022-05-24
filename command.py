import socket
import pickle


class Command:
    def __init__(self, index, data):
        if data:
            self.data = data
        self.index = index
