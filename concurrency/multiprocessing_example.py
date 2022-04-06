from multiprocessing import Process, Lock, Value
from multiprocessing.sharedctypes import Synchronized



def incrementer(n: int, lock: Lock, counter: Synchronized):
    for i in range(n):
        lock.acquire()
        counter.value += 1
        lock.release()

class Child(Process):
    def __init__(self, n: int, lock: Lock, counter: Synchronized):
        super().__init__()
        self.n = n
        self.lock = lock
        self.counter = counter

    def run(self) -> None:
        self.incrementer(self.n,self.lock, self.counter)

    def incrementer(self, n: int, lock: Lock, counter: Synchronized):
        for i in range(n):
            lock.acquire()
            counter.value += 1
            lock.release()

if __name__ == '__main__':
    counter = Value("i",0)
    lock = Lock()
    p0 = Child(1_000_000, lock, counter)
    p1 = Process(target=incrementer,args=(1_000_000, lock, counter))
    p2 = Process(target=incrementer,args=(1_000_000, lock, counter))
    p0.start()

    p1.start()
    p2.start()
    [p.join() for p in [p1, p2, p0]]
    print("Correct counter",counter.value)