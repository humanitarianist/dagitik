import socket
import threading
import Queue
import time

class serverReadThread(threading.Thread):

    def __init__(self, anotherPeerClientSocket, serverQueue, connectPoint, connectPointList):
        threading.Thread.__init__(self)
        self.anotherPeerClientSocket = anotherPeerClientSocket
        self.serverQueue = serverQueue
        self.connectPoint = connectPoint
        self.connectPointList = connectPointList


    def parser(self, data):

        if " " in data:
            indexRouter = data.index(" ")
            command = data[:indexRouter]
            arguments = data[indexRouter+1:]
        else:
            command = data
            arguments = None

        if command == "HELLO\n":
            lock1.acquire()
            self.serverQueue.put("SALUT N\n")
            lock1.release()

        elif command == "CLOSE\n":
            lock1.acquire()
            self.serverQueue.put("BUBYE\n")
            lock1.release()

        elif command == "REGME":
            indexRouter = arguments.index(":")
            ipNo = arguments[:indexRouter]
            portNo = data[indexRouter+1:]

            lock2.acquire()
            self.connectPoint = [ipNo, portNo, "W"]

            i = 0
            registered = False
            for point in self.connectPointList:
                if point[i][0] == self.connectPoint[0] and point[i][1] == self.connectPoint[1]:
                    lock1.acquire()
                    self.serverQueue.put("REGOK " + time.time())
                    lock1.release()
                    registered = True
                    self.connectPoint = []
                i += 1

            lock2.release()

            if registered == False:
                lock1.acquire()
                self.serverQueue.put("REGWA\n")
                lock1.release()

        elif command == "GETNL":

            if self.connectPoint[2] != "S":
                lock1.acquire()
                self.serverQueue.put("REGER\n")
                lock1.release()
            else:
                lock1.acquire()
                self.serverQueue.put("NLIST BEGIN\n")

                if arguments == None:
                    i = 0
                    lock3.acquire()
                    for point in self.connectPointList:
                        self.serverQueue.put(point[i][0] + ":" + point[i][1] + ":" + point[i][3] + ":P")
                        i += 1
                    lock3.release()
                else:
                    i = 0
                    lock3.acquire()
                    for point in self.connectPointList:
                        if i < arguments:
                            self.serverQueue.put(point[i][0] + ":" + point[i][1] + ":" + point[i][3] + ":P")
                            i += 1
                        else:
                            break
                    lock3.release()
                self.serverQueue.put("NLIST END\n")
                lock1.release()

    def run(self):
        while True:
            data = self.anotherPeerClientSocket.recv()
            self.parser(data)



class serverWriteThread(threading.Thread):

    def __init__(self, anotherPeerClientSocket, serverQueue):
        threading.Thread.__init__(self)
        self.anotherPeerClientSocket = anotherPeerClientSocket
        self.serverQueue = serverQueue

    def run(self):

        while True:
            lock1.acquire()
            if not serverQueue.empty():
                response = serverQueue.get()
                lock1.release()
                self.anotherPeerClientSocket.send(response)
            else:
                lock1.release()


class clientReadThread(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        pass



class clientWriteThread(threading.Thread):

    def __init__(self, connectPoint, connectPointList, peerClientSocket, serverQueue):
        threading.Thread.__init__(self)
        self.connectPoint = connectPoint
        self.connectPointList = connectPointList
        self.peerClientSocket = peerClientSocket
        self.serverQueue = serverQueue

    def run(self):

        if not self.connectPoint:
            anotherPeerServerSocketHost = self.connectPoint[1]
            anotherPeerServerSocketPort = self.connectPoint[0]

            try:
                self.peerClientSocket.connect(anotherPeerServerSocketHost, anotherPeerServerSocketPort)
                self.connectPoint[2] = "S"
                self.connectPoint[3] = time.time()
                lock3.acquire()
                self.connectPointList.append(self.connectPoint)
                lock3.release()
            except:
                lock1.acquire()
                self.serverQueue.put("REGER\n")
                lock1.release()



connectPointList = []
# connectPointList korumak icin
lock3 = threading.Lock()

peerServerSocket = socket.socket()

peerServerSocketHost = socket.gethostname()
peerServerSocketPort = 9090

peerServerSocket.bind((peerServerSocketHost, peerServerSocketPort))
peerServerSocket.listen(5)


threads = []

while True:
    serverQueue = Queue.Queue()
    # serverQueue korumak icin
    lock1 = threading.Lock()

    connectPoint = []
    # serverQueue korumak icin
    lock2 = threading.Lock()

    peerClientSocket = socket.socket()
    anotherPeerClientSocket, anotherPeerClientAddr = peerServerSocket.accept()

    lock3.acquire()
    srThread = serverReadThread(anotherPeerClientSocket, serverQueue, connectPoint, connectPointList)
    lock3.release()

    swThread = serverWriteThread(anotherPeerClientSocket, serverQueue)

    crThread = clientReadThread()

    lock3.acquire()
    cwThread = clientWriteThread(connectPoint, connectPointList, peerClientSocket, serverQueue)
    lock3.acquire()

    threads.append(srThread)
    threads.append(swThread)
    threads.append(crThread)
    threads.append(cwThread)

    srThread.start()
    swThread.start()
    crThread.start()
    cwThread.start()

for i in threads:
    i.join()