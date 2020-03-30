from random import randint
from time import sleep

from fei.ppds import Mutex, Event, Thread, print


class EventBarrier:
    def __init__(self, n):
        self.n = n
        self.counter = 0
        self.mutex = Mutex()
        self.event = Event()

    def barrier(self):
        self.mutex.lock()
        self.counter += 1
        if self.counter == self.n:
            self.counter = 0
            self.event.set()
            self.event.clear()
            self.mutex.unlock()
        else:
            self.mutex.unlock()
            self.event.wait()


def barrier_example(barrier, thread_id):
    sleep(randint(0, 10) / 10)
    print(f'Thread {thread_id} in front of barrier.')
    barrier.barrier()
    print(f'Thread {thread_id} leaving barrier.')


def main():
    N = 5
    barrier = EventBarrier(N)
    threads = [Thread(barrier_example, barrier, i) for i in range(N)]

    for t in threads:
        t.join()


if __name__ == "__main__":
    main()
