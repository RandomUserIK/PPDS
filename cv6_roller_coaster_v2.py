from random import randint
from time import sleep

from fei.ppds import Thread, Mutex, Semaphore, print


# viacero vlacikov, nemozu sa predbiehat
# iba 1 nastupiste, ale run() moze byt vykonavana KONKURENTNE (dokonca az PARALELNE)
# nesmu sa predbiehat - pouzijeme to iste co pri barber-fifo, resp. pole semaforov
# zavedieme 2 polia semaforov - loading_area, unloading_area
# v poli tolko semaforov, kolko je vlacikov
# v jednom case iba 1 semafor aktivny


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
        self.boarded = Semaphore(0)
        self.unboarded = Semaphore(0)
        self.barrier = Barrier(self.c)


def car(shared):
    while True:
        # otvorenie dveri
        load()
        shared.board_queue.signal(shared.c)

        # musi cakat, kym sa mu neoznami, ze vsetci nastupili
        shared.boarded.wait()  # posledny, ktory nastupi, by mal toto signalizovat

        # pusti jazdu
        run()

        # pusti pasazierov
        unload()
        shared.unboard_queue.signal(shared.c)

        # musi cakat, kym vsetci neodidu
        shared.unboarded.wait()


def passenger(shared, id_passenger):
    while True:
        # nemoze nastupit, kym ich vlacik nepusti -> cakanie vo fronte na nastup
        shared.board_queue.wait()

        # nastupi
        board(id_passenger)

        # musi C pasazierov nastupit
        shared.barrier.wait(shared.boarded)

        # nemoze vystupit, kym vlacik neurobi unboard()
        shared.unboard_queue.wait()

        # vystupi
        unboard(id_passenger)

        shared.barrier.wait(shared.unboarded)


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
