from random import randint
from time import sleep

from fei.ppds import Thread, Mutex, Semaphore, print


# specialna bariera - umoznuje prechadzat rieku iba istym kombinaciam vlakien
# lodka nesmie opustit breh inak, nez ked je naplnena
# cakanie a potrebujeme formovat kolko ktorych - FRONTA pomocou semaforov
# ale nevieme si vypocitat kolko ich je -> POCITADLO -> MUTEX
# ked potrebujeme aby jedno vlakno nieco spravilo - potrebujeme ho specialne oznacit
# toto oznacenie je lokalna premenna, ktora sa nastavi podla nejakeho STAVU


class SimpleBarrier:
    def __init__(self, n):
        self.n = n
        self.counter = 0
        self.mutex = Mutex()
        self.barrier = Semaphore(0)

    def wait(self):
        self.mutex.lock()
        self.counter += 1
        if self.counter == self.n:
            self.counter = 0
            self.barrier.signal(self.n)
        self.mutex.unlock()
        self.barrier.wait()


class Shared:
    def __init__(self):
        self.hackers = 0
        self.serfs = 0
        self.mutex = Mutex()
        self.hackers_queue = Semaphore(0)
        self.serfs_queue = Semaphore(0)
        self.barrier = SimpleBarrier(4)


def board(who, _id):
    print(f'{who} {_id}: boarded.')
    sleep(randint(50, 300) / 100)


def row_boat(who, _id):
    print(f'{who} {_id}: rowing.')
    sleep(randint(50, 300) / 100)


def hacker(shared, hacker_id):
    is_captain = False  # nemoze byt zdielana premenna, kedze iba 1 vlakno moze byt kapitan
    while True:
        shared.mutex.lock()
        shared.hackers += 1
        if shared.hackers == 4:
            # ak by bolo opacne, tato podmienka by bola pravdiva iba ak by pocet serfov bol mensi nez 2
            is_captain = True
            shared.hackers = 0
            shared.hackers_queue.signal(4)
        elif shared.hackers == 2 and shared.serfs >= 2:
            is_captain = True
            shared.hackers = 0
            shared.serfs -= 2
            # nemozeme nulovat, moze prist 200 serfov a po nich iba pridu hackeri, tu len urcite vieme ze su dvaja
            shared.hackers_queue.signal(2)  # ten kto robi signal, obehne ostatnych
            shared.serfs_queue.signal(2)
        else:
            shared.mutex.unlock()

        # cakanie na brehu
        shared.hackers_queue.wait()
        board('Hacker', hacker_id)
        shared.barrier.wait()  # cakanie !! - zaruci ze vsetci su pripraveni

        if is_captain:
            row_boat('Hacker', hacker_id)
            is_captain = False  # inak moze dvakrat odomknut mutex
            shared.mutex.unlock()  # po doveslovani - zarucuje ze nikto sa nebude nalodovat


def serf(shared, serf_id):
    is_captain = False
    while True:
        shared.mutex.lock()
        shared.serfs += 1
        if shared.serfs == 4:
            is_captain = True
            shared.serfs = 0
            shared.serfs_queue.signal(4)
        elif shared.serfs == 2 and shared.hackers >= 2:
            is_captain = True
            shared.serfs = 0
            shared.hackers -= 2
            shared.hackers_queue.signal(2)
            shared.serfs_queue.signal(2)
        else:
            shared.mutex.unlock()

        shared.serfs_queue.wait()
        board('Serf', serf_id)
        shared.barrier.wait()  # ak by bola poziadavka: kym kapitan neskonci veslovanie,
        # potrebovali by sme dvojitu barieru

        if is_captain:
            row_boat('Serf', serf_id)
            is_captain = False  # inak moze dvakrat odomknut mutex
            shared.mutex.unlock()


def main():
    shared = Shared()
    for i in range(5):
        Thread(hacker, shared, i)
        Thread(serf, shared, i)


if __name__ == "__main__":
    main()
