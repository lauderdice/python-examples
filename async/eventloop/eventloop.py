from typing import Generator, Tuple
from collections import deque

def countdown(n: int, identifier: str) -> Generator[Tuple[int, str], None, None]:
    while n > 0:
        yield n, identifier
        n -= 1



def run_event_loop(tasks: deque[Generator]):
    while tasks:
        current_task = tasks.popleft()
        try:
            number, identifier = next(current_task)
            print(identifier, number)
            tasks.append(current_task)
        except StopIteration:
            print("Task finished")

if __name__ == '__main__':
    q = deque([countdown(10, "first"), countdown(5, "second"), countdown(12, "third")])
    run_event_loop(q)