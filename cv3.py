from fei.ppds import Thread, Mutex, Semaphore, print

from random import randint
from time import sleep


class Lightswitch:
    def __init__(self):
        self.mutex = Mutex()
        self.counter = 0

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


class SharedRW:
    def __init__(self):
        self.readLS = Lightswitch()
        self.roomEmpty = Semaphore()
        # to avoid starvation we add turnstile
        self.turnstile = Semaphore()


def reader(shared_rw, thread_id):
    while True:
        shared_rw.turnstile.wait()
        shared_rw.turnstile.signal()
        shared_rw.readLS.lock(shared_rw.roomEmpty)
        # reader critical section
        print("Thread %s reading" % thread_id)
        sleep(2)
        shared_rw.readLS.unlock(shared_rw.roomEmpty)


def writer(shared_rw, thread_id):
    while True:
        shared_rw.turnstile.wait()
        shared_rw.roomEmpty.wait()
        # writer critical section
        print("Thread %s writing" % thread_id)
        sleep(2)
        shared_rw.turnstile.signal()
        shared_rw.roomEmpty.signal()


def writer_v2(shared_rw, thread_id):
    while True:
        shared_rw.turnstile.wait()
        shared_rw.roomEmpty.wait()
        # writer critical section
        print("Thread %s writing" % thread_id)
        sleep(2)
        shared_rw.turnstile.signal()
        shared_rw.roomEmpty.signal()


shared_rw = SharedRW()
readers = [Thread(reader, shared_rw, str(i)) for i in range(5)]
writers = [Thread(writer, shared_rw, str(i)) for i in range(5)]

for r in readers:
    r.join()

for w in writers:
    w.join()


class Shared:
    def __init__(self, buffer_size):
        self.mutex = Mutex()
        self.items = Semaphore()
        self.free = Semaphore(buffer_size)

    def produce(self, thread_id):
        sleep(randint(0, 10) / 10)
        print("Thread %s producing" % thread_id)

    def consume(self, thread_id):
        sleep(randint(0, 10) / 10)
        print("Thread %s consuming" % thread_id)


def producer(shared, thread_id):
    shared.produce(thread_id)
    shared.free.wait()
    shared.mutex.lock()
    # add to buffer
    shared.mutex.unlock()
    shared.items.signal()


def consumer(shared, thread_id):
    shared.items.wait()
    shared.mutex.lock()
    # pop from buffer
    shared.mutex.unlock()
    shared.free.signal()
    shared.consume(thread_id)


# shared = Shared(5)
# producers = [Thread(producer, shared, str(i)) for i in range(5)]
# consumers = [Thread(consumer, shared, str(i)) for i in range(5)]
#
# for p in producers:
#     p.join()
#
# for c in consumers:
#     c.join()



