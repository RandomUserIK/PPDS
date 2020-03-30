from random import randint
from time import sleep

from fei.ppds import Mutex, Semaphore, Thread, print


class Shared:
    def __init__(self, n):
        self.n = n
        self.counter = 0
        self.mutex = Mutex()
        self.turnstile1 = Semaphore(0)
        self.turnstile2 = Semaphore(1)


def rendezvous(thread_id):
    sleep(randint(1, 10) / 10)
    print(f'rendezvous: {thread_id}')


def ko(thread_id):
    print(f'ko: {thread_id}')
    sleep(randint(1, 10) / 10)


def barrier(shared, thread_id):
    while True:
        rendezvous(thread_id)

        shared.mutex.lock()
        shared.counter += 1
        if shared.counter == shared.n:
            shared.turnstile2.wait()
            shared.turnstile1.signal()
        shared.mutex.unlock()
        shared.turnstile1.wait()
        shared.turnstile1.signal()

        ko(thread_id)

        shared.mutex.lock()
        shared.counter -= 1
        if shared.counter == 0:
            shared.turnstile1.wait()
            shared.turnstile2.signal()
        shared.mutex.unlock()
        shared.turnstile2.wait()
        shared.turnstile2.signal()


def main():
    N = 5
    shared = Shared(N)
    threads = [Thread(barrier, shared, i) for i in range(N)]

    for t in threads:
        t.join()


if __name__ == "__main__":
    main()
