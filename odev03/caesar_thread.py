import threading

s, n, l = 1, 6, 10
order, k = 0, 1
class MyThread (threading.Thread):

    def __init__(self, threadID):
        threading.Thread.__init__(self)
        self.threadID = threadID

    def run(self):
        getline()

def getline():
    global order
    print thread.threadID
    workfinish = False
    while workfinish is False:
        newtextline = ""
        lock_key.acquire()
        textoneline = rfl.readline()
        thread.threadID = order
        order+=1
        lock_key.release()
        lenline = len(textoneline)
        bigtextline = textoneline.upper()
        if lenline is not 0:
            for i in bigtextline:
                for j in range(0, 26):
                    if i is alphabet[j]:
                        newtextline += alphabet[(j + s) % 26]
                    elif i in [',', '.', ' ', '(', ')', '-', '"', '*', ':', "\n"] or i in '0123456789':
                        newtextline += i
                        break
            newwrite(newtextline,order)
        else:
            workfinish = True

def newwrite(textline,o):
    key = False
    global k
    if k == o:
        wfl.write(textline)
        k+=1
        if key:
            lock_key.release()
            key = False
    else:
        lock_key.acquire()
        key = True
        newwrite(textline,o)

alphabet  = "ABCDEFGHIJKLMNOPQRSTUVWXYZ" + "\n"
lock_key = threading.Lock()
threads = []

rfl = open("metin.txt", "r")
wfl = open("crypted_" + repr(s) + "_" + repr(n) + "_" + repr(l) + ".txt", 'w')

# Create new threads
for tID in range(0, n):
    thread = MyThread(tID)
    thread.start()
    threads.append(thread)

# Wait for all threads to complete
for t in threads:
    t.join()

rfl.close()
wfl.close()