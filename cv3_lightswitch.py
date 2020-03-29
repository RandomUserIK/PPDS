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
        self.mutex.lock()


def main():
    pass


if __name__ == "__main__":
    main()