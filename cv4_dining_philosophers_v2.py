from random import randint
from time import sleep

from fei.ppds import Thread, Semaphore, print

PHILOSOPHERS = 5


class Shared:
    def __init__(self):
        self.forks = [Semaphore(1) for i in range(PHILOSOPHERS)]


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


def get_forks_leftie(shared, philosopher_id):
    print(f'Philosopher (leftie) {philosopher_id}: getting forks.')
    shared.forks[left(philosopher_id)].wait()
    shared.forks[right(philosopher_id)].wait()


def get_forks_rightie(shared, philosopher_id):
    print(f'Philosopher (rightie) {philosopher_id}: getting forks.')
    shared.forks[right(philosopher_id)].wait()
    shared.forks[left(philosopher_id)].wait()


def put_forks_leftie(shared, philosopher_id):
    print(f'Philosopher (leftie) {philosopher_id}: putting forks.')
    shared.forks[left(philosopher_id)].signal()
    shared.forks[right(philosopher_id)].signal()


def put_forks_rightie(shared, philosopher_id):
    print(f'Philosopher (rightie) {philosopher_id}: putting forks.')
    shared.forks[right(philosopher_id)].signal()
    shared.forks[left(philosopher_id)].signal()


def philosopher_leftie(shared, philosopher_id):
    while True:
        think(philosopher_id)
        get_forks_leftie(shared, philosopher_id)
        eat(philosopher_id)
        put_forks_leftie(shared, philosopher_id)


def philosopher_rightie(shared, philosopher_id):
    while True:
        think(philosopher_id)
        get_forks_rightie(shared, philosopher_id)
        eat(philosopher_id)
        put_forks_rightie(shared, philosopher_id)


def main():
    shared = Shared()
    philosophers_lefties = [Thread(philosopher_leftie, shared, i) for i in range(PHILOSOPHERS - 1)]
    philosophers_righties = [Thread(philosopher_leftie, shared, 4)]

    for p in philosophers_lefties + philosophers_righties:
        p.join()


if __name__ == "__main__":
    main()
