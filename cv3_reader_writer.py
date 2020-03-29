from fei.ppds import Thread, Mutex, Semaphore, print

from random import randint
from time import sleep


class LightSwitch:
    def __init__(self):
        self.counter = 0
        self.mutex = Mutex()

    def lock(self, semaphore):
        self.mutex.lock()
        self.counter += 1
        if self.counter == 1:
            semaphore.wait()
        self.mutex.unlock()

    def unlock(self, semaphore):
        self.mutex.lock()
        self.counter -= 1
        if self.counter == 0:
            semaphore.signal()
        self.mutex.unlock()


class Shared:
    def __init__(self):
        self.room_empty = Semaphore(1)
        self.turnstile = Semaphore(1)  # to avoid starvation
        self.read_ls = LightSwitch()


def reading(thread_id):
    print(f'Thread {thread_id}: reading.')
    sleep(randint(0, 10)/10)


def writing(thread_id):
    print(f'Thread {thread_id}: writing.')
    sleep(randint(15, 25) / 10)


def reader(shared, thread_id):
    while True:
        shared.turnstile.wait()
        shared.turnstile.signal()

        shared.read_ls.lock(shared.room_empty)
        reading(thread_id)
        shared.read_ls.unlock(shared.room_empty)


def writer(shared, thread_id):
    while True:
        shared.turnstile.wait()
        shared.room_empty.wait()
        writing(thread_id)
        # shared.turnstile.signal()  - less effective
        shared.room_empty.signal()
        shared.turnstile.signal()


def main():
    shared = Shared()
    readers = [Thread(reader, shared, i) for i in range(10)]
    writers = [Thread(writer, shared, i) for i in range(5)]

    for t in readers + writers:
        t.join()


if __name__ == "__main__":
    main()
