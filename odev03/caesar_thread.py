import threading
import Queue


class MyThread (threading.Thread):
    def __init__(self, threadID):
        lock_key1.acquire()
        threading.Thread.__init__(self)
        self.threadID = threadID
        lock_key1.release()

    def run(self):
        getline()


def getline():
    lock_key1.acquire()
    textoneline = rfl.readline()
    threadqueue.put(thread.threadID)
    encode(thread.threadID, textoneline, len(textoneline))
    lock_key1.release()


def encode(Id, line, lenght):
    newline = ""
    bigline = line.upper()
    for i in bigline:
        if i in "0123456789.,'^+%&/()=?_-*\";:><|\}][{$#\n\t ":
            newline += i
            continue
        for j in alphabet:
            if i is j:
                newline += alphabet[(alphabet.index(j) + s) % 26]
                break
    putline(Id, newline, lenght)


def putline(Id, codeline, lenght):
    global a
    dizi.append(threadqueue.get())
    lock_key2.acquire()
    if Id is dizi[0]:
        wfl.write(codeline)
        del dizi[0]
    else:
        putline(id, codeline, lenght)

    lock_key2.release()
    a = lenght

s, n = 1, 6
alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
threadqueue = Queue.Queue()
lock_key1, lock_key2 = threading.Lock(), threading.Lock()
threads = []
dizi = []
a = 1

rfl = open("metin.txt", "r")
wfl = open("crypted_" + repr(s) + "_" + repr(n) + "_" + "line" + ".txt", 'w')

# Create new threads
for tID in range(0, n):
    thread = MyThread(tID)
    thread.start()
    threads.append(thread)

# Wait for all threads to complete
for t in threads:
    t.join()


while a is not 0:
    # Create new threads
    for tID in range(0, n):
        thread = MyThread(tID)
        thread.start()
        threads.append(thread)


# Wait for all threads to complete
    for t in threads:
        t.join()

wfl.close()
rfl.close()
