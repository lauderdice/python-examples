from typing import Generator


def fib() -> Generator:
    current, nxt = 0, 1
    while True:
        current, nxt = nxt, current + nxt
        yield current


result = fib()

for n in result:
    print(n, end=', ')
    if n > 10000:
        break

