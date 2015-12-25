#!/usr/bin/env python
import socket
import threading
import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import Queue
import time

class readThread (threading.Thread):

    def __init__(self, serverSocket, app):
        threading.Thread.__init__(self)
        self.serverSocket = serverSocket
        self.app = app

    def incomingParser(self, data):

        if len(data) == 0:
            return

        if len(data) > 3 and not data[3] == " ":
            print data + "a1"
            response = "ERR"
            self.serverSocket.send(response)
            return

        elif data[0:3] == "ERL":
            self.app.cprint("Server: Giris yapilmadi.")

        elif data[0:3] == "ERR":
            print "a2"
            self.app.cprint("Server: Eksik veya hatali komut")

        elif data[0:3] == "HEL":
            self.app.cprint("Server: " + data[4:] + " oturuma katildiniz")

        elif data[0:3] == "REJ":
            self.app.cprint("Server: " + data[4:] + " kullanicisi oturumda mevcut. Baska bir nickname ile giris yapmalisiniz.")

        elif data[0:3] == "LSA":
            splitted = data[4:].split(":")
            msg = "Server: -Kayitli kullanicilar- "
            for i in splitted:
                msg += i + ","
            msg = msg[:-1]

        elif data[0:3] == "MNO":
            self.app.cprint("Server: Boyle bir nickname'e sahip kulllanici bulunmamaktadir.")

        if " " in data[4:]:
            indexRouter = data[4:].index(" ")
            fromWho = data[4:indexRouter]
            message = data[indexRouter+1:]

            if ":" in fromWho:
                indexRouter = data[4:].index(":")
                fromWho = data[4:indexRouter]

        if data[0:3] == "SAY":
            self.app.cprint("<" + fromWho + ">" + message)


        if data[0:3] == "MSG":
            self.app.cprint("''" + fromWho + "''" + message)


    def run(self):
        while True:
            fromServer = self.serverSocket.recv(1024)
            self.incomingParser(fromServer)
            print fromServer
            if fromServer[0:3] == "BYE":
                break


class writeThread (threading.Thread):

    def __init__(self, serverSocket):
        threading.Thread.__init__(self)
        self.serverSocket = serverSocket

    def run(self):
        while True:

            fromClient = sendQueue.get()

            self.serverSocket.send(fromClient)
            if fromClient[0:3] == "QUI":
                break


class clientDialog(QDialog):
    ''' An example application for PyQt. Instantiate and call the run method to run. '''

    def __init__(self, threadQueue):

        self.threadQueue = threadQueue

        # create a Qt application --- every PyQt app needs one
        self.qt_app = QApplication(sys.argv)

        # Call the parent constructor on the current object
        QDialog.__init__(self, None)

        # Set up the window
        self.setWindowTitle('IRC Client')
        self.setMinimumSize(500, 200)

        # Add a vertical layout
        self.vbox = QVBoxLayout()

        # The sender textbox
        self.sender = QLineEdit("", self)

        # The channel region
        self.channel = QTextBrowser()

        # The send button
        self.send_button = QPushButton('&Send')

        # Connect the Go button to its callback
        self.send_button.clicked.connect(self.outgoing_parser)

        # Add the controls to the vertical layout
        self.vbox.addWidget(self.channel)
        self.vbox.addWidget(self.sender)
        self.vbox.addWidget(self.send_button)

        # A very stretchy spacer to force the button to the bottom
        # self.vbox.addStretch(100)
        # Use the vertical layout for the current window
        self.setLayout(self.vbox)

    def cprint(self, data):
        self.channel.append(data)

    def outgoing_parser(self):
        # textbox'tan qstring cekiyoruz
        data = self.sender.text()

        # qstring'i string'e ceviriyoruz
        data = str(data)

        if len(data) == 0:
            return

        self.cprint("Local: " + data)

        if data[0] == "/":

            if " " in data:
                indexRouter = data.index(" ")
                command = data[1:indexRouter]
                arguments = data[indexRouter+1:]
            else:
                command = data[1:]
                arguments = None

            if command == "nick":
                self.threadQueue.put("USR " + arguments)

            elif command == "list":
                self.threadQueue.put("LSQ")

            elif command == "msg":
                indexRouter = arguments.index(" ")
                toNickname = arguments[1:indexRouter]
                message = arguments[indexRouter+1:]
                self.threadQueue.put("MSG " + toNickname + ":" + message)

            elif command == "quit":
                self.threadQueue.put("QUI")

            else:
                self.cprint("Local: Command Error.")

        else:
            self.threadQueue.put("SAY " + data)

        self.sender.clear()

    def run(self):
        ''' Run the app and show the main form. '''
        self.show()
        self.qt_app.exec_()

serverSocket = socket.socket()

host = socket.gethostname()
port = 12345

serverSocket.connect((host, port))

sendQueue = Queue.Queue()
app = clientDialog(sendQueue)

rThread = readThread(serverSocket, app)
wThread = writeThread(serverSocket)

rThread.start()
wThread.start()
app.run()
rThread.join()
wThread.join()