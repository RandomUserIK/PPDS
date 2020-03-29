from fei.ppds import Mutex, Semaphore, Thread, print

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


def rendezvous(thread_id):
    sleep(randint(1, 10) / 10)
    print(f'rendezvous: {thread_id}')


def ko(thread_id):
    print(f'ko: {thread_id}')
    sleep(randint(1, 10) / 10)


def barrier(b, thread_id):
    while True:
        rendezvous(thread_id)
        b.barrier()
        ko(thread_id)
        b.barrier()


N = 5
b = SimpleBarrier(N)
threads = [Thread(barrier, b, i) for i in range(N)]