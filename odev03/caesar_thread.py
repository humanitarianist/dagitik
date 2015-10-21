import threading
import Queue

class MyThread (threading.Thread):
    def __init__(self, threadID):
        threading.Thread.__init__(self)
        with lock_key1:
                    self.threadID = threadID

    def run(self):
        getline()
        lock_key1.acquire()
        print thread.threadID
        lock_key1.release()

def getline():
    lock_key1.acquire()
    textoneline = rfl.readline()
    threadqueue.put(thread.threadID)
    encode(thread.threadID,textoneline,len(textoneline))
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
                newline += alphabet[alphabet.index(j)]
                break
    putline(Id, newline,lenght)

def putline(id, codeline, lenght):
    dizi.append(threadqueue.get())
    lock_key2.acquire()
    if  id is dizi[0]:
        wfl.write(codeline)
        del dizi[0]
    else:
        putline(id, codeline, lenght)
    if lenght > 0:
        thread.threadID += 6
        getline()

    lock_key2.release()

s, n = 1, 6
alphabet  = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
threadqueue = Queue.Queue()
lock_key1, lock_key2 = threading.Lock(), threading.Lock()
threads = []
dizi = []

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


wfl.close()
rfl.close()