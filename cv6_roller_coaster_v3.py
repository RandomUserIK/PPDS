from random import randint
from time import sleep

from fei.ppds import Thread, Mutex, Semaphore, print


class Barrier:
    def __init__(self, n):
        self.n = n
        self.counter = 0
        self.mutex = Mutex()
        self.semaphore = Semaphore(0)

    def wait(self, last_signal: Semaphore):
        self.mutex.lock()
        self.counter += 1
        if self.counter == self.n:
            self.counter = 0
            self.semaphore.signal(self.n)
            last_signal.signal()  # nezalezi na poradi, nevieme ovplyvnit oblast ktora sa vykonava konkurentne
        self.mutex.unlock()
        self.semaphore.wait()


class Shared:
    def __init__(self, c):
        self.c = c
        self.board_queue = Semaphore(0)
        self.unboard_queue = Semaphore(0)
        self.change = Semaphore(0)
        self.barrier = Barrier(self.c)


def car(shared):
    while True:
        # otvorenie dveri
        load()
        shared.board_queue.signal(shared.c)

        # musi cakat, kym sa mu neoznami, ze vsetci nastupili
        shared.change.wait()  # posledny, ktory nastupi, by mal toto signalizovat

        # pusti jazdu
        run()

        # pusti pasazierov
        unload()
        shared.unboard_queue.signal(shared.c)

        # musi cakat, kym vsetci neodidu
        shared.change.wait()


def passenger(shared, id_passenger):
    while True:
        # nemoze nastupit, kym ich vlacik nepusti -> cakanie vo fronte na nastup
        shared.board_queue.wait()

        # nastupi
        board(id_passenger)

        # musi C pasazierov nastupit
        shared.barrier.wait(shared.change)

        # nemoze vystupit, kym vlacik neurobi unboard()
        shared.unboard_queue.wait()

        # vystupi
        unboard(id_passenger)

        shared.barrier.wait(shared.change)


def load():
    print("Train loading passengers.")
    # load iba ako signalizacia, oneskorenie na strane pasazierov


def unload():
    print("Train unloading passengers.")


def board(id_passenger):
    print(f"Passenger {id_passenger}: boarded.")
    sleep(randint(50, 200) / 100)


def unboard(id_passenger):
    print(f"Passenger {id_passenger}: unboarded.")
    sleep(randint(50, 200) / 100)


def run():
    print("Train running.")
    sleep(randint(50, 300) / 100)


def main():
    c = 4
    shared = Shared(c)
    for i in range(5):
        Thread(passenger, shared, i)

    Thread(car, shared)


if __name__ == "__main__":
    main()
