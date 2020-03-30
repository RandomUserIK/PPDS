from random import randint
from time import sleep

from fei.ppds import Thread, Mutex, Semaphore, print


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
        self.no_writers = Semaphore(1)
        self.no_readers = Semaphore(1, 'fifo')
        self.read_ls = LightSwitch()
        self.write_ls = LightSwitch()


def reading(thread_id):
    print(f'Thread {thread_id}: reading.')
    sleep(randint(0, 10)/10)


def writing(thread_id):
    print(f'Thread {thread_id}: writing.')
    sleep(randint(15, 25) / 10)


def reader(shared, thread_id):
    while True:
        shared.no_readers.wait()

        shared.read_ls.lock(shared.no_writers)

        shared.no_readers.signal()  # tymto zarucime, aby r() nebol predbehnuty w()

        reading(thread_id)
        shared.read_ls.unlock(shared.no_writers)


def writer(shared, thread_id):
    while True:
        shared.write_ls.lock(shared.no_readers)

        shared.no_writers.wait()
        writing(thread_id)
        shared.no_writers.signal()

        shared.write_ls.unlock(shared.no_readers)


def main():
    shared = Shared()
    readers = [Thread(reader, shared, i) for i in range(10)]
    writers = [Thread(writer, shared, i) for i in range(5)]

    for t in readers + writers:
        t.join()


if __name__ == "__main__":
    main()
