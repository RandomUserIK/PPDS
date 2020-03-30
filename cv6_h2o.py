from random import randint, choice
from time import sleep

from fei.ppds import Thread, Mutex, Semaphore, print


# potreba za barierou - kazde vlakno musi cakat pokym sa nebude moct vytvorit molekula
# musia sa pockat predtym nez povolia dalsej trojici pokracovat
# pouzitie scoreboardu
# ked frontu modelujeme semaforom - na zaciatku init 0
# asymetricke riesenie synchronizacie - mutex sa odomkyna iba na strane kyslika
# co H2O3 ? --> river crossing


class Barrier:
    def __init__(self, n):
        self.n = n
        self.counter = 0
        self.mutex = Mutex()
        self.barrier1 = Semaphore(0)
        self.barrier2 = Semaphore(0)

    def wait(self):
        self.mutex.lock()
        self.counter += 1
        if self.counter == self.n:
            print('-------')
            self.barrier1.signal(self.n)
        self.mutex.unlock()
        self.barrier1.wait()

        self.mutex.lock()
        self.counter -= 1
        if self.counter == 0:
            self.barrier2.signal(self.n)
        self.mutex.unlock()
        self.barrier2.wait()


class Shared:
    def __init__(self):
        self.oxygen = 0
        self.hydrogen = 0
        self.mutex = Mutex()
        self.barrier = Barrier(3)
        self.oxyQueue = Semaphore(0)
        self.hydroQueue = Semaphore(0)


def bond(molecule_id):
    print(f"bond {molecule_id}")


def oxygen(shared):
    shared.mutex.lock()
    shared.oxygen += 1
    if shared.hydrogen < 2:
        shared.mutex.unlock()
    else:
        shared.oxygen -= 1
        shared.hydrogen -= 2
        shared.oxyQueue.signal(1)
        shared.hydroQueue.signal(2)

    shared.oxyQueue.wait()
    bond('O')
    shared.barrier.wait()

    shared.mutex.unlock()


def hydrogen(shared):
    shared.mutex.lock()
    shared.hydrogen += 1
    if shared.oxygen < 1 or shared.hydrogen < 2:
        shared.mutex.unlock()
    else:
        shared.oxygen -= 1
        shared.hydrogen -= 2
        shared.oxyQueue.signal(1)
        shared.hydroQueue.signal(2)

    shared.hydroQueue.wait()
    bond('H')
    shared.barrier.wait()


def main():
    shared = Shared()

    while True:
        Thread(choice([oxygen, hydrogen]), shared)
        sleep(randint(0, 3)/100)


if __name__ == "__main__":
    main()