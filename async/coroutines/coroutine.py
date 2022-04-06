import asyncio


class AwaitableInt:

    def __init__(self,val: int):
        self.val: int = val
    def __await__(self):
        yield self.val

# native coroutine
async def coro():
    for i in range(5):
        await AwaitableInt(i)

# original coroutine from Python 2 having yield on right side - it has to be initialized by next()
def coro2():
    print ("Will print what is received as input")
    while True:
        line = (yield)
        print("I received: ",line)


c = coro()
print(c)
print(type(c))
print(c.send(None))
print(c.send(None))
print(c.send(None))
print(c.send(None))
print(c.send(None))

c2 = coro2()
print(c2)
print(type(c2))
c2.send(None) # initialization
c2.send("Ahoj")


@asyncio.coroutine # coroutine decorator initializes the coroutine
def py34_coro():
    """Generator-based coroutine, older syntax - deprecated"""
    yield from AwaitableInt(5)

async def py35_coro():
    """Native coroutine, modern syntax"""
    await AwaitableInt(5)


