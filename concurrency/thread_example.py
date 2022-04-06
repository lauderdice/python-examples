from threading import Lock
from threading import Thread

def incrementer(n: int, lock: Lock):
    global counter
    for i in range(n):
        lock.acquire()
        counter += 1
        lock.release()
def incrementer_bad(n: int):
    global counter
    for i in range(n):
        counter += 1


counter = 0
thread1 = Thread(target=incrementer_bad,args=(1_000_000,))
thread2 = Thread(target=incrementer_bad,args=(1_000_000,))
thread1.start()
thread2.start()
[t.join() for t in [thread1, thread2]]
print("Bad counter", counter)

counter = 0
lock = Lock()
thread1 = Thread(target=incrementer,args=(1_000_000,lock))
thread2 = Thread(target=incrementer,args=(1_000_000,lock))
thread1.start()
thread2.start()
[t.join() for t in [thread1, thread2]]
print("Good counter", counter)


