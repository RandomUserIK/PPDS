from fei.ppds import Mutex, Event, Thread, print

from random import randint
from time import sleep


class Shared:
    def __init__(self, n):
        self.n = n
        self.counter = 0
        self.mutex = Mutex()
        self.event = Event()
        self.event.signal()
        self.elem_arr = [0, 1] + [0] * self.n


def compute_element(shared, thread_id):
    shared.elem_arr[thread_id + 2] = shared.elem_arr[thread_id + 1] + shared.elem_arr[thread_id]


def fibonacci(shared, thread_id):
    while True:
        shared.mutex.lock()
        if shared.counter == thread_id:
            compute_element(shared, thread_id)
            shared.counter += 1
            shared.event.signal()
            shared.event.clear()
            shared.mutex.unlock()
            break
        else:
            shared.mutex.unlock()
            shared.event.wait()


def main():
    N = 10
    shared = Shared(N)
    threads = [Thread(fibonacci, shared, i) for i in range(N)]

    for t in threads:
        t.join()

    print(shared.elem_arr)


if __name__ == "__main__":
    main()
