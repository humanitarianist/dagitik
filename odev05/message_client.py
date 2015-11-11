#!/usr/bin/env python
import socket
import threading

class readThread (threading.Thread):

    def __init__(self, clientSocket):
        threading.Thread.__init__(self)
        self.clientSocket = clientSocket

    def run(self):
        while True:
            fromServer = self.clientSocket.recv(1024)
            lastinst = "BYE"
            if(lastinst in fromServer):
                break
            else:
                print fromServer


class writeThread (threading.Thread):

    def __init__(self, clientSocket):
        threading.Thread.__init__(self)
        self.clientSocket = clientSocket

    def run(self):
        while True:
            fromClient = raw_input()
            lastInst = "QUI"
            self.clientSocket.send(fromClient)
            if fromClient == lastInst:
                break


clientSocket = socket.socket()

host = socket.gethostname()
port = 12346

clientSocket.connect((host, port))

rThread = readThread(clientSocket)
wThread = writeThread(clientSocket)

rThread.start()
wThread.start()

rThread.join()
wThread.join()