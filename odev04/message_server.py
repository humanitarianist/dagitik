#!/usr/bin/env python
# -*- encoding: ISO8859-10 -*-

import socket
import threading
import datetime
import random

class myThread (threading.Thread):

    def __init__(self, threadID, clientSocket, clientAddr):
        threading.Thread.__init__(self)
        self.clientSocket = clientSocket
        self.clientAddr = clientAddr
        self.threadID = threadID

    def run(self):
        print "Starting Thread-" + str(self.threadID)
        print "Waiting for connection"
        ConnectClient(self)
        print "Ending Thread-" + str(self.threadID)
        print "Waiting for connection"

def ConnectClient(self):
    time = int(round(20*random.random())) + 1
    threshold  = time
    self.clientSocket.send("Merhaba, saat þu an %s" % datetime.datetime.now().strftime("%H:%M:%S"))
    print
    while True:
        time += 1
        if time%threshold == 0:
            self.clientSocket.send("Merhaba, saat þu an %s" % datetime.datetime.now().strftime("%H:%M:%S"))
            time = int(round(20*random.random())) + 1
            threshold = time
        fromClient = self.clientSocket.recv(1024)
        lastInst = "end"
        if(fromClient != lastInst):
            self.clientSocket.send("Peki " + repr(self.clientAddr[1]))
        else:
            self.clientSocket.send(lastInst)
            break

def showTime():
    time = int(round(20*random.random())) + 1

key = threading.Lock()
ServerSocket = socket.socket()
host = socket.gethostname()
port = 1234
ServerSocket.bind((host, port))
threadID = 0
haveConnection = 0
threads = []
ServerSocket.listen(5)

while True:
    if threadID == 0:
        print "Waiting for connection"
    clientSocket, addr = ServerSocket.accept()
    print 'Got a connection from ', addr
    threadID += 1
    thread = myThread(threadID, clientSocket, addr)
    threads.append(thread)
    thread.start()
    showTime()

for i in threads:
    i.join()
