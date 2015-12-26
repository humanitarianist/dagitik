import socket
import threading
import Queue
import time

class serverReadThread(threading.Thread):

    def __init__(self, peerClientSocket, serverQueue, connectPoint, connectPointList):
        threading.Thread.__init__(self)
        self.peerClientSocket = peerClientSocket
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

            lock4.acquire()
            self.connectPoint = [ipNo, portNo, "W"]
            lock4.release()

            lock1.acquire()
            self.serverQueue.put("REGWA\n")
            lock1.release()

        elif command == "GETNL":
            lock4.acquire()
            if self.connectPoint[2] != "S":
                lock4.release()
                lock1.acquire()
                self.serverQueue.put("REGER\n")
                lock1.release()
            else:
                lock4.release()
                lock1.acquire()
                self.serverQueue.put("NLIST BEGIN\n")

                if arguments == None:
                    j = 0
                    lock3.acquire()
                    for i in self.connectPointList:
                        self.serverQueue.put(self.connectPointList[j][0] + ":" + self.connectPointList[j][1] + ":" + self.connectPointList[j][3] + ":P")
                        j += 1
                    lock3.release()
                else:
                    j = 0
                    lock3.acquire()
                    for i in self.connectPointList:
                        if j < arguments:
                            self.serverQueue.put(self.connectPointList[j][0] + ":" + self.connectPointList[j][1] + ":" + self.connectPointList[j][3] + ":P")
                            j += 1
                        else:
                            break
                    lock3.release()
                self.serverQueue.put("NLIST END\n")
                lock1.release()

    def run(self):
        while True:
            data = self.peerClientSocket.recv()
            self.parser(data)



class serverWriteThread(threading.Thread):

    def __init__(self, peerClientSocket, serverQueue):
        threading.Thread.__init__(self)
        self.peerClientSocket = peerClientSocket
        self.serverQueue = serverQueue

    def run(self):

        while True:
            lock1.acquire()
            if not serverQueue.empty():
                response = serverQueue.get()
                lock1.release()
                self.peerClientSocket.send(response)
            else:
                lock1.release()


class clientReadThread(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        pass



class clientWriteThread(threading.Thread):

    def __init__(self, connectPoint, connectPointList, negotiatorClientSocket, peerClientSocket):
        threading.Thread.__init__(self)
        self.connectPoint = connectPoint
        self.connectPointList = connectPointList
        self.negotiatorClientSocket = negotiatorClientSocket
        self.peerClientSocket = peerClientSocket

    def run(self):

        while True:
            lock4.acquire()
            if not self.connectPoint:

                peerServerSocketHost = self.connectPoint[1]
                peerServerSocketPort = self.connectPoint[0]

                try:
                    self.negotiatorClientSocket.connect(peerServerSocketHost, peerServerSocketPort)
                    self.connectPoint[2] = "S"
                    self.connectPoint[3] = time.time()
                    lock3.acquire()
                    self.connectPointList.append(self.connectPoint)
                    lock3.release()
                    lock4.release()
                except:
                    lock4.release()
                    lock3.acquire()
                    self.connectPointList.remove(self.connectPoint)
                    lock3.release()
                    self.peerClientSocket.send("REGER\n")





connectPointList = []
# connectPointList korumak icin
lock3 = threading.Lock()

negotiatorServerSocket = socket.socket()

negotiatorServerSocketHost = socket.gethostname()
negotiatorServerSocketPort = 9090

negotiatorServerSocket.bind((negotiatorServerSocketHost, negotiatorServerSocketPort))
negotiatorServerSocket.listen(5)


threads = []

while True:
    serverQueue = Queue.Queue()
    # serverQueue korumak icin
    lock1 = threading.Lock()

    connectPoint = []
    # connectPoint korumak icin
    lock4 = threading.Lock()

    negotiatorClientSocket = socket.socket()
    peerClientSocket, peerClientAddr = negotiatorServerSocket.accept()

    lock3.acquire()
    srThread = serverReadThread(peerClientSocket, serverQueue, connectPoint, connectPointList)
    lock3.release()

    swThread = serverWriteThread(peerClientSocket, serverQueue)

    crThread = clientReadThread()

    lock3.acquire()
    cwThread = clientWriteThread(connectPoint, connectPointList, negotiatorClientSocket, peerClientSocket)
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