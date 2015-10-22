from multiprocessing import Lock, Process, Queue

def getline():
    lock_key1.acquire()
    textoneline = rfl.readline()
    processqueue.put(p.pid)
    encode(Id, textoneline, len(textoneline))
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
    dizi.append(processqueue.get())
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
processqueue = Queue()
lock_key1, lock_key2 = Lock(), Lock()
process = []
dizi = []
a = 1
Id = 0

rfl = open("metin.txt", "r")
wfl = open("crypted_" + repr(s) + "_" + repr(n) + "_" + "line" + ".txt", 'w')

while a is not 0:
    # Create new process
    for tID in range(0, n):
        p = Process(target = getline)
        p.start()
        Id+=1


    for tID in range(0, n):
        p.join()


wfl.close()
rfl.close()
