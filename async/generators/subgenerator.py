import random
from typing import Generator, Coroutine


def reader() -> Generator:
    for i in range(5):
        yield i


def readerwrapper_old_syntax(query: Generator) -> Generator:
    for i in query:
        yield i

# is equal to

def readerwrapper_new_syntax(query: Generator) -> Generator:
    yield from query

q = reader()

for i in q:
    print(i)
for i in readerwrapper_new_syntax(reader()):
    print(i)
for i in readerwrapper_old_syntax(reader()):
    print(i)


def writer() -> Coroutine:
    while True:
        w = (yield)
        print("writing: ", w)

def writer_wrapper_old(coro: Coroutine) -> Coroutine:
    coro.send(None)  # initialize coroutine
    while True:
        try:
            x = (yield)  # Capture the value that is sent
            coro.send(x)  # and pass it to the writer
        except StopIteration:
            pass

def writer_wrapper_new(coro: Coroutine) -> Coroutine:
    yield from coro


print()
w = writer()
wrap = writer_wrapper_old(w)
wrap.send(None)  # initialize
for i in range(4):
    wrap.send(i)

w = writer()
wrap = writer_wrapper_new(w)
wrap.send(None)  # initialize

for i in range(4):
    wrap.send(i)

def inner_generator() -> Generator:
    yield "This will be yielded on the first call to next() of the outer generator"
    return "This will be the returned value assigned to the left hand side of the outer generator"


def outer_generator() -> Generator:
    returned_value = yield from inner_generator()
    print(returned_value)
    return

outer = outer_generator()
print("First call to next() yielded: ",next(outer))
next(outer)
