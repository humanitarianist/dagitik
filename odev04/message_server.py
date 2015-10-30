#!/usr/bin/env python

import socket
import threading
import datetime


class myThread (threading.Thread):

    def __init__(self, threadID, clientSocket, clientAddr):
        threading.Thread.__init__(self)
        self.clientSocket = clientSocket
        self.clientAddr = clientAddr
        self.threadID = threadID

    def run(self):
        print "Starting Thread-" + str(self.threadID)
        ConnectClient(self)
        print "Ending Thread-" + str(self.threadID)


def ConnectClient(self):
    self.clientSocket.send("Merhaba, saat su an %s" % datetime.datetime.now().strftime("%H:%M:%S"))
    while True:
        a = self.clientSocket.recv(1024)
        b = "end"
        if(a != b):
            self.clientSocket.send("Peki " + repr(self.clientAddr[1]))
        else:
            self.clientSocket.send(b)
            break

key = threading.Lock()
ServerSocket = socket.socket()
host = socket.gethostname()
port = 1234
ServerSocket.bind((host, port))
threadID = 0
threads = []
ServerSocket.listen(5)

while True:
    clientSocket, addr = ServerSocket.accept()
    print 'Got a connection from ', addr
    threadID += 1
    thread = myThread(threadID, clientSocket, addr)
    threads.append(thread)
    thread.start()

for i in threads:
    i.join()
