#!/usr/bin/env python
# -*- encoding: ISO8859-10 -*-

import socket
import threading
import Queue
import time


class readThread (threading.Thread):

    def __init__(self, threadName, nickname, threadID, clientSocket, clientAddr, fihrist, threadQueue, logQueue):
        threading.Thread.__init__(self)
        self.threadName = "read" + threadName
        self.nickname = nickname
        self.threadID = threadID
        self.clientSocket = clientSocket
        self.clientAddr = clientAddr
        self.fihrist = fihrist
        self.threadQueue = threadQueue
        self.logQueue = logQueue

    def Parser(self, data):
        data = data.strip()

        # henuz giris yapmamis ise ve giris yapmadan islem yapmak isterse "ERL" dondur
        if not self.nickname and not data[0:3] == "USR":
            response = "ERL"
            return [response, 0]

        # Daha onceden login olmus ise ve login halinde tekrar login olmak istiyorsa "ERL" dondur
        elif self.nickname and data[0:3] == "USR":
            response = "ERL"
            return [response, 0]

        # Kullanici giris yapmak istiyorsa
        elif data[0:3] == "USR" :
            self.nickname = data[4:]

            # Nickname vermeden giris yapmak isterse
            if not self.nickname:
                response = "ERL"
                return [response, 0]

            # Nickname kullanima uygunsa
            lock1.acquire()
            if not self.fihrist.has_key(self.nickname):
                response = "HEL " + self.nickname
                self.fihrist[self.nickname] = self.threadQueue
                lock2.acquire()
                self.logQueue.put(self.nickname + " has joined.")
                lock2.release()
                lock1.release()
                return [response, 0]

            # Nickname kullanima uygun degilse
            else:
                # kullanici reddedilecek
                response = "REJ " + self.nickname
                self.nickname = None
                lock1.release()
                return [response, 0]

        # Kullanici cikis yapmak istiyorsa
        elif data[0:3] == "QUI":
            response = "BYE " + self.nickname

            lock1.acquire()
            for i in fihrist.keys():
                self.fihrist[i].put(self.nickname + " kullanicisi oturumu sonlandirdi.")
            lock1.release()

            # fihristten sil
            lock1.acquire()
            del fihrist [self.nickname]
            lock1.release()
            # baglantiyi sil
            return [response, 1]

        # Kullanici diger kullanicilari listelemek istiyorsa
        elif data[0:3] == "LSQ":
            response = "LSA "
            lock1.acquire()
            for i in fihrist.keys():
                response += i + ": "
            lock1.release()
            response = response.strip(": ")
            return [response, 0]

        # Baglanti kontrol komutu
        elif data[0:3] == "TIC":
            response = "TOC"
            return [response, 0]

        # Kullanici genel mesaj yollamak isterse
        elif data[0:3] == "SAY":
            queue_message = (self.nickname, data[4:])
            lock1.acquire()
            for i in fihrist.keys():
                self.fihrist[i].put(queue_message)
            lock1.release()
            response = ""
            return [response, 0]

        # Kullanici ozel mesaj yollamak isterse
        elif data[0:3] == "MSG":

            # ":" karakterini koymayi unutmus ise
            if not ":" in data:
                response = "ERR"
                return [response, 0]

            # to_nickname'i ve mesaji ayikla
            indexRouter = data.index(":")
            to_nickname = data[4:indexRouter]
            message = data[indexRouter+1:]

            # Eger kisi listede yoksa
            lock1.acquire()
            if not to_nickname in self.fihrist.keys():
                response = "MNO " + to_nickname
                lock1.release()
                return [response, 0]

            # Kisi mevcutsa mesaji kisinin kuyruguna ekle
            else:
                queue_message = (to_nickname, self.nickname, message)
                # gonderilecek threadQueueyu fihristten alip icine yaz
                self.fihrist[to_nickname].put(queue_message)
                response = "MOK"
                lock1.release()
                return [response, 0]

        # bir seye uymadiysa protokol hatasi verilecek
        else:
            response = "ERR"
            return [response, 0]

    def run(self):
        self.logQueue.put("Starting " + self.threadName)
        while True:

            incomingData = self.clientSocket.recv(1024)

            # Istemciye cevap hazirlaniyor.
            reaction = self.Parser(incomingData)
            # Istemciye cevap yollaniyor.
            self.clientSocket.send(reaction[0])

            # Istemci cikmak isterse soket kapaniyor.
            if reaction[1] == 1:
                self.clientSocket.close()
                break
        # log gonder
        self.logQueue.put(self.nickname + " has left.")
        self.logQueue.put("Exiting " + self.threadName)

class writeThread (threading.Thread):

    def __init__(self, threadName, nickname, threadID, clientSocket, clientAddr, fihrist, threadQueue, logQueue):
        threading.Thread.__init__(self)
        self.threadName = "read" + threadName
        self.nickname = nickname
        self.threadID = threadID
        self.clientSocket = clientSocket
        self.clientAddr = clientAddr
        self.fihrist = fihrist
        self.threadQueue = threadQueue
        self.logQueue = logQueue

    def run(self):
        self.logQueue.put("Starting " + self.threadName)

        while True:
            if not threadQueue.empty():
                message = threadQueue.get()
                if len(message) == 1:
                    message = "SYS " + message

                elif len(message) == 2:
                    message = "SAY " + message[0] + " " + message[1]

                elif len(message) == 3:
                    message = "MSG " + message[0] + ":" + message[1] + " " + message[2]

                self.clientSocket.send(message)


class loggerThread (threading.Thread):
    def __init__(self, threadName, logQueue, logFileName):
        threading.Thread.__init__(self)
        self.threadName = threadName
        self.logQueue = logQueue
        self.logFileName = logFileName
        # dosyayi appendable olarak ac
        self.fid = open(logFileName, 'a+')

    def log(self,message):
        # gelen mesaji zamanla beraber bastir
        t = time.ctime()
        self.fid.write(("%s: %s\n"  %(t, message)))
        self.fid.flush()

    def run(self):
        self.log("Starting " + self.threadName)
        while True:
            time.sleep(10000)
            if not logQueue.empty():
                lock2.acquire()
                to_be_logged =  logQueue.get()
                lock2.release()
                self.log(to_be_logged)

        self.log("Exiting" + self.threadName)
        self.fid.close()

serverSocket = socket.socket()
host = socket.gethostname()
port = 12345
serverSocket.bind((host, port))
serverSocket.listen(5)

threadID = 0
threads = []

fihrist = {}
logQueue = Queue.Queue()

lThread = loggerThread("Logger Thread", logQueue, "LogFile")
threads.append(lThread)
lThread.start()

# fihristi korumak icin
lock1 = threading.Lock()
# logQueue korumak icin
lock2 = threading.Lock()

while True:
    clientSocket, clientAddr = serverSocket.accept()
    connectionString = 'Got a connection from ' + repr(clientAddr)
    logQueue.put(connectionString)
    threadID += 1
    threadName = "Thread-" + repr(threadID)
    threadQueue = Queue.Queue()
    rThread = readThread(threadName ,None ,threadID, clientSocket, clientAddr, fihrist, threadQueue, logQueue)
    wThread = writeThread(threadName ,None ,threadID, clientSocket, clientAddr, fihrist, threadQueue, logQueue)
    threads.append(rThread)
    threads.append(wThread)
    rThread.start()
    wThread.start()

for i in threads:
    i.join()
