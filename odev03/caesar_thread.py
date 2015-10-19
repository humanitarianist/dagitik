
import threading

s, n, l = 1, 6, 10
k, m = 0, 1
newtextline = []
textoneline = []
lenline = []


class MyThread (threading.Thread):
    def __init__(self, threadID):
        threading.Thread.__init__(self)
        self.threadID = threadID

    def run(self):
        process_data()

def process_data():
    exitFlag = False
    while not exitFlag:
        lock_key.acquire()
        k = (k + 1) % 6
        lock_key.release()
        textoneline[k] = rfl.readline()
        lenline[k] = len(textoneline[k])
        textoneline[k].upper()
        if lenline[k] is not 0:
            for i in range(0, lenline[k]):
                for j in range(0, 26):
                    if textoneline[i] is alphabet[j]:
                        newtextline[k][i] = alphabet[(j + s) % 26]
                        break
        else:
            exitFlag = True

        while k is not m:
            pass

        wfl.write(newtextline[k])
        m = m + 1

alphabet  = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
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
