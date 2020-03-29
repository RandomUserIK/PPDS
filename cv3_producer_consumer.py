from fei.ppds import Thread, Mutex, Semaphore, print

from random import randint
from time import sleep


class Shared:
    def __init__(self, buffer_size):
        self.mutex = Mutex()
        self.items = Semaphore(0)
        self.free = Semaphore(buffer_size)

    def produce(self, thread_id):
        print(f'Thread {thread_id}: producing.')
        sleep(randint(5, 15)/10)

    def consume(self, thread_id):
        print(f'Thread {thread_id}: consuming.')
        sleep(randint(5, 10)/10)


def add_to_buffer(thread_id):
    print(f'Thread {thread_id}: adding to buffer.')
    sleep(randint(0, 10) / 10)


def remove_from_buffer(thread_id):
    print(f'Thread {thread_id}: removing from buffer.')
    sleep(randint(0, 10) / 10)


def producer(shared, thread_id):
    while True:
        shared.produce(thread_id)
        shared.free.wait()

        shared.mutex.lock()
        add_to_buffer(thread_id)
        shared.mutex.unlock()

        shared.items.signal()


def consumer(shared, thread_id):
    while True:
        shared.items.wait()

        shared.mutex.lock()
        remove_from_buffer(thread_id)
        shared.mutex.unlock()

        shared.free.signal()
        shared.consume(thread_id)


def main():
    shared = Shared(10)
    n_producers = 5
    n_consumers = 3

    producers = [Thread(producer, shared, i) for i in range(n_producers)]
    consumers = [Thread(consumer, shared, i) for i in range(n_consumers)]

    for t in producers + consumers:
        t.join()


if __name__ == "__main__":
    main()