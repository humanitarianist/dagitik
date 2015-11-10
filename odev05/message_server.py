
import socket
import threading
import time
import Queue

def parser(self, data):
    data = data.strip()

    # henuz login olmadiysa
    if not self.nickname and not data[0:3] == "USR":
        response = "ERL"
        self.clientSocket.send()
        return response

    elif data[0:3] == "USR":
        nickname = data[4:]
        if not fihrist.has_key(nickname):
            # kullanici yoksa
            response = "HEL " + nickname
            self.fihrist[nickname] = self.tQueue
            # fihristi guncelle
            fihrist.update(self.fihrist)
            self.lQueue.put(self.nickname + " has joined.")
            return 0
        else:
            # kullanici reddedilecek
            response = "REJ " + nickname
            self.csend(response)
            # TOD
            # baglantiyi kapat
            self.csoc.close()
            return

    elif data[0:3] == "QUI":
        response = "BYE " + self.nickname
        # TOD
        # fihristten sil
        # TOD
        # log gonder
        # TOD
        # baglantiyi sil
        # TOD
    elif data[0:3] == "LSQ":
        response = "LSA "
        # TOD
    elif data[0:3] == "TIC":
        # TOD
    elif data[0:3] == "SAY":
        # TOD
    elif data[0:3] == "MSG":
        # TOD
        if not to_nickname in self.fihrist.keys():
            response = "MNO
        else:
            queue_message = (to_nickname, self.nickname, message)
            # gonderilecek threadQueueyu fihristten alip icine yaz
            self.fihrist[to_nickname].put(queue_message)
            response = "MOK"
        self.csend(response)
    else:
        # bir seye uymadiysa protokol hatasi verilecek
        response = "ERR"
        # TODO

class ReadThread (threading.Thread):
    def __init__(self, name, cSocket, address, logQueue):
        threading.Thread.__init__(self)
        self.name = name
        self.cSocket = cSocket
        self.address = address
        self.lQueue = logQueue
        self.fihrist = fihrist
        self.tQueue = Queue.Queue()



    def run(self):
        self.lQueue.put("Starting " + self.name)
        while True:

            # burasi blocking bir recv halinde duracak
            # gelen protokol komutlari parserdan gecirilip
            # ilgili hareketler yapilacak
            incomingData = self.clientSocket.recv(1024)

            queueMessage = parser(self, incomingData)

            # istemciye cevap h a z r l a .
            # TODO
            # cevap veya cevaplari gondermek üzere
            # threadQueue'ya yaz
            # lock mekanizmasini unutma
            # TODO
        self.lQueue.put("Exiting " + self.name)

class WriteThread (threading.Thread):
    def __init__(self, name, cSocket, address, threadQueue, logQueue ):
        threading.Thread.__init__(self)
        self.name = name
        self.cSocket = cSocket
        self.address = address
        self.lQueue = logQueue
        self.tQueue = threadQueue
    def run(self):
        self.lQueue.put("Starting " + self.name)
        while True:
            # TODO

            # burasi kuyrukta sirasi gelen mesajlari
            # gondermek icin kullanilacak
            if self.threadQueue.qsize() > 0:
                queue_message = self.threadQueue.get()

                # gonderilen ozel mesajsa
                if # TODO
                    message_to_send = "MSG " +  # TODO

                # genel mesajsa
                elif queue_message[1]:
                    message_to_send = "SAY " + # TODO

                # hicbiri degilse sistem mesajidir
                else:
                    message_to_send = "SYS " + # TODO

            # TODO
        self.lQueue.put("Exiting " + self.name)

class LoggerThread (threading.Thread):
    def __init__(self, name, logQueue, logFileName):
        threading.Thread.__init__(self)
        self.name = name
        self.lQueue = logQueue
        # dosyayi appendable olarak ac
        self.fid = # TODO

    def log(self,message):
        # gelen mesaji zamanla beraber bastir
        t = time.ctime()
        self.fid.write(t + # TODO)
        self.fid.flush()

    def run(self):
        self.log("Starting " + self.name)

        while True:
            # TODO
            # lQueue'da yeni mesaj varsa
            # self.log() metodunu cagir

            to_be_logged = # TODO
            self.log(to_be_logged)

        self.log("Exiting" + self.name)
        self.fid.close()

serverSocket = socket.socket()
host = socket.gethostname()
port = 12345
serverSocket.bind((host, port))

# Her istemcinin isminin ve mesaj kuyruklarinin tutulacagi kuyruk
fihrist = {}

# Loglarin sirasiyla tutulmasini saglamak icin olusturulan log kuyrugu
logQueue = Queue.Queue()

# Acilan her thread' in tutulacagi threads listesi
threads = []


while True:
    clientSocket, addr = serverSocket.accept()
    rThread = ReadThread(" ", clientSocket, addr, logQueue)
    wThread = WriteThread()

    threads.append(rThread)
    threads.append(wThread)

    rThread.start()
    wThread.start()