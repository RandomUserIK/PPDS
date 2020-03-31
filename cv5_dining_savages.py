from fei.ppds import Thread, Mutex, Semaphore, print

from random import randint
from time import sleep


# scoreboard
# pristuo ako v pripade producent - konzument


class Shared:
    def __init__(self, n):
        self.servings = n
        self.mutex = Mutex()
        self.empty_pot = Semaphore(0)
        self.full_pot = Semaphore(0)

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
        shared.mutex.lock()
        if shared.servings == 0:
            print(f'Savage {savage_id}: waking cook.')
            shared.empty_pot.signal()
            shared.full_pot.wait()
        shared.get_serving_from_pot(savage_id)
        shared.mutex.unlock()
        eat(savage_id)


def cook(shared):
    while True:
        # netreba mutex, lebo jeden divoch caka na full_pot a drzi mutex
        # ostatni divosi su teda na mutexe zablokovani
        # ak by sme mutex pouzili, nastal by deadlock
        shared.empty_pot.wait()
        print(f'Cook: cooking.')
        sleep(randint(50, 200) / 100)
        shared.put_serving_in_pot(10)
        shared.full_pot.signal()


def main():
    shared = Shared(10)
    [Thread(savage, shared, i) for i in range(10)]
    Thread(cook, shared)


if __name__ == "__main__":
    main()
