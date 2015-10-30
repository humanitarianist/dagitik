#!/usr/bin/env python
import socket
import threading

class readThread (threading.Thread):

    def __init__(self, clientSocket):
        threading.Thread.__init__(self)
        self.clientSocket = clientSocket

    def run(self):
        while True:
            a = self.clientSocket.recv(1024)
            b = "end"
            if(a == b):
                break
            else:
                print a


class writeThread (threading.Thread):

    def __init__(self, clientSocket):
        threading.Thread.__init__(self)
        self.clientSocket = clientSocket

    def run(self):
        while True:
            a = raw_input()
            b = "end"
            self.clientSocket.send(a)
            if a == b:
                break

clientSocket = socket.socket()

host = socket.gethostname()
port = 1234

clientSocket.connect((host, port))

rThread = readThread(clientSocket)
wThread = writeThread(clientSocket)

rThread.start()
wThread.start()

rThread.join()
wThread.join()