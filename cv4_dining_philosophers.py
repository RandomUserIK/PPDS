from fei.ppds import Thread, Mutex, Semaphore, print

from random import randint
from time import sleep

PHILOSOPHERS = 5


class Shared:
    def __init__(self):
        self.forks = [Semaphore(1) for i in range(PHILOSOPHERS)]
        self.footman = Semaphore(4)


def right(philosopher_id):
    return philosopher_id


def left(philosopher_id):
    return (philosopher_id + 1) % PHILOSOPHERS


def eat(philosopher_id):
    print(f'Philosopher {philosopher_id}: eating.')
    sleep(randint(5, 10) / 10)


def think(philosopher_id):
    print(f'Philosopher {philosopher_id}: thinking.')
    sleep(randint(10, 15) / 10)


def get_forks(shared, philosopher_id):
    print(f'Philosopher {philosopher_id}: getting forks.')
    shared.footman.wait()
    shared.forks[right(philosopher_id)].wait()
    shared.forks[left(philosopher_id)].wait()


def put_forks(shared, philosopher_id):
    print(f'Philosopher {philosopher_id}: putting forks.')
    shared.forks[right(philosopher_id)].signal()
    shared.forks[left(philosopher_id)].signal()
    shared.footman.signal()


def philosopher(shared, philosopher_id):
    while True:
        think(philosopher_id)
        get_forks(shared, philosopher_id)
        eat(philosopher_id)
        put_forks(shared, philosopher_id)


def main():
    shared = Shared()
    philosophers = [Thread(philosopher, shared, i) for i in range(PHILOSOPHERS)]

    for p in philosophers:
        p.join()


if __name__ == "__main__":
    main()
