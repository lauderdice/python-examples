class AwaitableInt:

    def __init__(self,val: int):
        self.val: int = val
    def __await__(self):
        yield self.val

# native coroutine
async def coro():
    for i in range(5):
        await AwaitableInt(i)

c = coro()
print(c)
print(type(c))
print(c.send(None))
print(c.send(None))
print(c.send(None))
print(c.send(None))
print(c.send(None))


# generator based coroutine
def coro2():
    print ("Will print what is received as input")
    while True:
        line = (yield)
        print("I received: ",line)

c2 = coro2()
print(c2)
print(type(c2))
c2.send(None)
c2.send("Ahoj")