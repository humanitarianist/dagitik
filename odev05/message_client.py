#!/usr/bin/env python
import socket
import threading

class readThread (threading.Thread):

    def __init__(self, serverSocket):
        threading.Thread.__init__(self)
        self.serverSocket = serverSocket

    def run(self):
        while True:
            fromServer = self.serverSocket.recv(1024)
            lastinst = "BYE"
            if(lastinst in fromServer):
                print fromServer
                break
            else:
                print fromServer


class writeThread (threading.Thread):

    def __init__(self, serverSocket):
        threading.Thread.__init__(self)
        self.serverSocket = serverSocket

    def run(self):
        while True:
            fromClient = raw_input()
            lastInst = "QUI"
            self.serverSocket.send(fromClient)
            if fromClient[0:3] == lastInst:
                break


serverSocket = socket.socket()

host = socket.gethostname()
port = 12346

serverSocket.connect((host, port))

rThread = readThread(serverSocket)
wThread = writeThread(serverSocket)

rThread.start()
wThread.start()

rThread.join()
wThread.join()