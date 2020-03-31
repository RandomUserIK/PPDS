from fei.ppds import Thread, Mutex, Semaphore, print

from random import randint
from time import sleep


# divosi vzdy ZACINAJU vecerat vsetci spolu
# bariera - zacinaju nieco robit spolu, CAKANIE


class Barrier:
    def __init__(self, n):
        self.n = n
        self.counter = 0
        self.mutex = Mutex()
        self.barrier = Semaphore(0)

    def wait(self, savage_id, barrier_id):
        self.mutex.lock()
        self.counter += 1
        print(f'Savage {savage_id}: before barrier: {barrier_id}. {self.counter} savages present.')
        if self.counter == self.n:
            print(f'Savage {savage_id}: opening barrier: {barrier_id}')
            self.counter = 0
            self.barrier.signal(self.n)
        self.mutex.unlock()
        self.barrier.wait()


class Shared:
    def __init__(self, n, savages):
        self.servings = n
        self.mutex = Mutex()
        self.empty_pot = Semaphore(0)
        self.full_pot = Semaphore(0)
        self.barrier1 = Barrier(savages)
        self.barrier2 = Barrier(savages)

    def get_serving_from_pot(self, savage_id):
        print(f'Savage {savage_id}: taking a portion.')
        self.servings -= 1

    def put_serving_in_pot(self, n):
        print('Cook: put serving in pot.')
        self.servings += n


def eat(savage_id):
    print(f'Savage {savage_id}: eating a portion.')
    sleep(randint(50, 200) / 100)


def savage(shared, savage_id):
    while True:
        shared.barrier1.wait(savage_id, 1)
        shared.mutex.lock()
        if shared.servings == 0:
            print(f'Savage {savage_id}: waking cook.')
            shared.empty_pot.signal()
            shared.full_pot.wait()
        shared.get_serving_from_pot(savage_id)
        shared.mutex.unlock()
        eat(savage_id)
        shared.barrier2.wait(savage_id, 2)  # aby nenastalo obehnutie


def cook(shared):
    while True:
        shared.empty_pot.wait()
        print(f'Cook: cooking.')
        sleep(randint(50, 200) / 100)
        shared.put_serving_in_pot(10)
        shared.full_pot.signal()


def main():
    savages = 10
    shared = Shared(10, savages)
    [Thread(savage, shared, i) for i in range(savages)]
    Thread(cook, shared)


if __name__ == "__main__":
    main()