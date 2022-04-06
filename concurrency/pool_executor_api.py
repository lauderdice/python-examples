from concurrent.futures import ThreadPoolExecutor
from multiprocessing import Lock

counter = 0
def incrementer(n: int, lock: Lock):
    global counter
    for i in range(n):
        lock.acquire()
        counter += 1
        lock.release()
if __name__ == '__main__':

    lock = Lock()

    with ThreadPoolExecutor(max_workers=5) as executor:
        futures_list = []
        for i in range(2):
            future = executor.submit(incrementer,1_000_000, lock)
            futures_list.append(future)
        [f.result() for f in futures_list]
    print(counter)
