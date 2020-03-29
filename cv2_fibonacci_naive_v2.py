from fei.ppds import Semaphore, Thread, print

from random import randint
from time import sleep


class Shared:
    def __init__(self, n):
        self.n = n
        self.elem_arr = [0, 1] + [0] * self.n
        self.semaphores = [Semaphore(0) for i in range(self.n + 1)]
        self.semaphores[0].signal(1)


def compute_element(shared, thread_id):
    shared.elem_arr[thread_id + 2] = shared.elem_arr[thread_id + 1] + shared.elem_arr[thread_id]


def fibonacci(shared, thread_id):
    sleep(randint(0, 10) / 10)

    print(f"Thread {thread_id}: start.")
    shared.semaphores[thread_id].wait()

    print(f"Thread {thread_id}: computing element.")
    compute_element(shared, thread_id)

    shared.semaphores[thread_id + 1].signal()
    print(f"Thread {thread_id}: stop.")


N = 10
shared = Shared(N)
threads = [Thread(fibonacci, shared, i) for i in range(N)]

for t in threads:
    t.join()

print(shared.elem_arr)
