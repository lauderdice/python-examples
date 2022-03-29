"""
Comparison of old and new async syntax
"""
import time
from collections import deque
from typing import Generator, Coroutine

"""

"Under the hood" way - using the yield keyword

"""
class Scheduler:
    def __init__(self):
        self.ready: deque[Generator] = deque()
        self.current = None

    def new_task(self, gen: Generator):
        self.ready.append(gen)

    def run(self):
        while self.ready:
            self.current = self.ready.popleft()
            try:
                next(self.current)
                if self.current:
                    self.ready.append(self.current)
            except StopIteration:
                pass


sched = Scheduler()  # Background scheduler object

def countdown(n: int):
    while n > 0:
        print('Down', n,time.time())
        print("Down - before sleep",time.time())
        time.sleep(1)
        print("Down - after sleep, before yield",time.time())
        yield
        print("Down - after yield",time.time())
        n -= 1

def countup(stop: int):
    x = 0
    while x < stop:
        print('Up', x,time.time())
        print("Up - before sleep",time.time())
        time.sleep(1)
        print("Up - after sleep, before yield",time.time())
        yield
        print("Up - after yield",time.time())
        x += 1

# ------------------------------ running the old syntax way -------------------------------------
# provides no speedup
start = time.time()
sched.new_task(countdown(5))
sched.new_task(countup(5))
sched.run()
print("old loop took",time.time()-start)
# ------------------------------ end of the old syntax way ---------------------------------------

"""

"BELOW - The same thing but rewritten with async/await - newer syntax
replaced generators with coroutines, added async keyword to be able to use await

"""
class Awaitable:
    def __await__(self):
        yield

def switch():
    return Awaitable()

class SchedulerModern:
    def __init__(self):
        self.ready: deque[Coroutine] = deque()
        self.current = None

    def new_task(self, cor: Coroutine):
        self.ready.append(cor)

    def run(self):
        while self.ready:
            self.current = self.ready.popleft()
            try:
                # next(self.current) we no longer use next(generator) but send() to coroutine
                self.current.send(None)
                if self.current:
                    self.ready.append(self.current)
            except StopIteration:
                pass


sched = SchedulerModern()

async def countdown(n: int):
    while n > 0:
        print('Down', n,time.time())
        print("Down - before sleep",time.time())
        time.sleep(1)
        print("Down - after sleep, before yield",time.time())
        await switch() # if we want to use await keyword hiding the yield we have to declare the method as async
        print("Down - after yield",time.time())
        n -= 1

async def countup(stop: int):
    x = 0
    while x < stop:
        print('Up', x,time.time())
        print("Up - before sleep",time.time())
        time.sleep(1)
        print("Up - after sleep, before yield",time.time())
        await switch() # if we want to use await keyword hiding the yield we have to declare the method as async
        print("Up - after yield",time.time())
        x += 1

# ------------------------------ running the new syntax way -------------------------------------
# provides no speedup
start = time.time()
sched.new_task(countdown(5))
sched.new_task(countup(5))
sched.run()
print("modern loop took",time.time()-start)