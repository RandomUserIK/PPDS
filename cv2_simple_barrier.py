from fei.ppds import Mutex, Semaphore, Thread

from random import randint
from time import sleep


class SimpleBarrier:
    def __init__(self, n):
        self.n = n
        self.counter = 0
        self.mutex = Mutex()
        self.b = Semaphore(0)

    def barrier(self):
        self.mutex.lock()
        self.counter += 1
        if self.counter == self.n:
            self.counter = 0
            self.b.signal(self.n)
        self.mutex.unlock()
        self.b.wait()


def barrier_example(barrier, thread_id):
    sleep(randint(0, 10) / 10)
    print(f'Thread {thread_id} in front of barrier.')
    barrier.barrier()
    print(f'Thread {thread_id} leaving barrier.')


N = 5
barrier = SimpleBarrier(N)
threads = [Thread(barrier_example, barrier, i) for i in range(N)]