import threading

class MyThread (threading.Thread):
    def __init__(self, threadID):
        threading.Thread.__init__(self)
        self.threadID = threadID

    def run(self):
        getline()

def getline():
    global orderkey
    lock_key.acquire()
    textoneline = rfl.readline()
    print orderkey
    orderkey+=1

    encode(textoneline,orderkey-1)
    lock_key.release()
def encode(line, order):
    newline = ""
    if len(line) is not 0:
        bigline = line.upper()
        for i in bigline:
            if i in "0123456789.,'^+%&/()=?_-*\";:><|\}][{$#\n\t ":
                newline += i
                continue
            for j in alphabet:
                if i is j:
                    newline += alphabet[alphabet.index(j)]
                    break
        putline(newline,order)
        getline()

def putline(codeline,order):
    global orderline
    lock_key.acquire()
    workfinished = False
    if order >= len(orderline):
        for i in (len(orderline), order):
            orderline.append(codeline)
        print orderline
    else:
        del orderline[order]
        orderline.insert(order, codeline)
        print orderline
    lock_key.release()
    workfinished = True

s, n = 1, 6
alphabet  = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
lock_key = threading.Lock()
threads = []
orderkey = 0
orderline = []
workfinished = False

rfl = open("metin.txt", "r")
wfl = open("crypted_" + repr(s) + "_" + repr(n) + "_" + "line" + ".txt", 'w')

# Create new threads
for tID in range(0, n):
    thread = MyThread(tID)
    thread.start()
    threads = []
    threads.append(thread)


# Wait for all threads to complete
for t in threads:
    t.join()

for i in orderline:
    wfl.write(i)

wfl.close()