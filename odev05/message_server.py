#!/usr/bin/env python
# -*- encoding: ISO8859-10 -*-

import socket
import threading
import Queue


class readThread (threading.Thread):

    def __init__(self, nickname, threadID, clientSocket, clientAddr, fihrist, tQueue):
        threading.Thread.__init__(self)
        self.clientSocket = clientSocket
        self.clientAddr = clientAddr
        self.threadID = threadID
        self.nickname = nickname
        self.fihrist = fihrist
        self.tQueue = tQueue

    def run(self):
#        self.lQueue.put("Starting " + self.name)
        while True:

            # burasi blocking bir recv halinde duracak
            # gelen protokol komutlari parserdan gecirilip
            # ilgili hareketler yapilacak
            incomingData = self.clientSocket.recv(1024)

            reaction = Parser(self, incomingData)

            self.clientSocket.send(reaction[0])

            if reaction[1] == 1:
                self.clientSocket.close()
                break
        print "tamam"
            # istemciye cevap h a z r l a .
            # TODO
            # cevap veya cevaplari gondermek üzere
            # threadQueue'ya yaz
            # lock mekanizmasini unutma
            # TODO
#        self.lQueue.put("Exiting " + self.name)


def Parser(self, data):
    data = data.strip()

    # henuz giris yapmamis ise ve giris yapmadan islem yapmak isterse "ERL" ve 1 (hatali) dondur
    if not self.nickname and not data[0:3] == "USR":
        response = ["ERL", 0]
        return response

    # Daha onceden login olmus ise ve login halinde tekrar login olmak istiyorsa "ERL" ve 1 (hatali) dondur
    elif self.nickname and data[0:3] == "USR":
        response = ["ERL", 0]
        return response

    # Kullanici giris yapmak istiyorsa
    elif data[0:3] == "USR":
        self.nickname = data[4:]
        # Nickname kullanima uygunsa
        if not self.fihrist.has_key(self.nickname):
            response = "HEL " + self.nickname
            self.fihrist[self.nickname] = self.tQueue
#            self.lQueue.put(self.nickname + " has joined.")
            return [response, 0]
        # Nickname kullanima uygun degilse
        else:
            # kullanici reddedilecek
            response = "REJ " + self.nickname
            return [response, 0]

    # Kullanici cikis yapmak istiyorsa
    elif data[0:3] == "QUI":
        response = "BYE " + self.nickname
        # fihristten sil
        del fihrist [self.nickname]
        # log gonder
#        self.lQueue.put(self.nickname + " has left.")
        # baglantiyi sil
        return [response, 1]



    # Kullanici diger kullanicilari listelemek istiyorsa
    elif data[0:3] == "LSQ":
        response = "LSA "
        for i in fihrist.keys():
            response += i + ": "
        return [response, 0]

    # Baglanti kontrol komutu
    elif data[0:3] == "TIC":
        response = "TOC"
        return [response, 0]

    # Kullanici genel mesaj yollamak isterse
    elif data[0:3] == "SAY":
        for i in fihrist.keys():
            self.fihrist[i].put(data[4:])
        response = "SOK"
        return [response, 0]

    # Kullanici ozel mesaj yollamak isterse
    elif data[0:3] == "MSG":
        indexRouter = data.index(":")

        if indexRouter < 0:
            response = "ERR"
            return [response, 0]
        else:
            to_nickname = data[4:indexRouter]
            message = data[indexRouter:]

        if not to_nickname in self.fihrist.keys():
            response = "MNO " + to_nickname
            return [response, 0]
        else:
            queue_message = (to_nickname, self.nickname, message)
            # gonderilecek threadQueueyu fihristten alip icine yaz
            self.fihrist[to_nickname].put(queue_message)
            response = "MOK"
            return [response, 0]

    else:
        # bir seye uymadiysa protokol hatasi verilecek
        response = "ERR"
        return [response, 0]

serverSocket = socket.socket()
host = socket.gethostname()
port = 12346
serverSocket.bind((host, port))
serverSocket.listen(5)

threadID = 0
threads = []

fihrist = {}
tQueue = Queue.Queue()

while True:
    clientSocket, addr = serverSocket.accept()
    print 'Got a connection from ', addr
    threadID += 1
    rThread = readThread(None ,threadID, clientSocket, addr, fihrist, tQueue)
#    wThread = writeThread(threadID, clientSocket, addr)
    threads.append(rThread)
#    threads.append(wThread)
    rThread.start()
 #   wThread.start()

for i in threads:
    i.join()
