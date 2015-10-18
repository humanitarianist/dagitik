import Queue
import threading
import time

s, n, l = 1, 6, 10
exitFlag = False;

class MyThread (threading.Thread):
    def __init__(self, threadID, name, q):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.q = q

    def run(self):
        process_data()

def process_data():
    while not exitFlag:
        lock_key.acquire()
        if not workQueue.empty():
            data = q.get()
            queueLock.release()
            print "%s processing %s" % (threadName, data)
        else:
            queueLock.release()
        time.sleep(1)

alphabet  = "abcdefghijklmnopqrstuvwxyz"
lock_key = threading.Lock()
threads = []

fl = open("metin.txt", "r")

# Create new threads
for tID in range(0, n):
    thread = MyThread(tID)
    thread.start()
    threads.append(thread)

# Fill the queue
queueLock.acquire()
for word in nameList:
    workQueue.put(word)
queueLock.release()

# Wait for queue to empty
while not workQueue.empty():
    pass

# Notify threads it's time to exit
exitFlag = 1

# Wait for all threads to complete
for t in threads:
    t.join()
print "Exiting Main Thread"