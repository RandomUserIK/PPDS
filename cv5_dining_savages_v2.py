from time import sleep

from fei.ppds import Thread, Mutex, Semaphore, print

MAX_PORTIONS = 3
SAVAGES = 3
COOKS = 2


class Shared:
    def __init__(self):
        self.savage_mutex = Mutex()
        self.cook_mutex = Mutex()
        self.portions = 0
        self.cook_counter = 0
        self.full_pot = Semaphore(0)
        self.empty_pot = Semaphore(0)


def get_portion(shared, savage_id):
    print(f"Savage {savage_id}: get portion.")
    sleep(0.3)
    shared.portions -= 1


def put_portion(shared, cook_id):
    print(f"Cook {cook_id}: put portion.")
    sleep(0.3)
    shared.portions += 1


def cooking(cook_id):
    print(f"Cook {cook_id}: cooking.")
    sleep(0.3)


def savage(shared, savage_id):
    while True:
        shared.savage_mutex.lock()
        if shared.portions == 0:
            print(f"Savage {savage_id}: waking cooks.")
            shared.empty_pot.signal(COOKS)
            shared.full_pot.wait()
        get_portion(shared, savage_id)
        shared.savage_mutex.unlock()


def cook(shared, cook_id):
    while True:
        shared.empty_pot.wait()
        cooking(cook_id)
        shared.cook_mutex.lock()
        shared.cook_counter += 1
        if shared.portions == MAX_PORTIONS and shared.cook_counter == COOKS:
            print(f'Cook {cook_id}: waking up savages.')
            shared.full_pot.signal()
            shared.cook_counter = 0
        elif shared.portions < MAX_PORTIONS:
            put_portion(shared, cook_id)
            if shared.cook_counter == COOKS:
                shared.cook_counter = 0
                shared.empty_pot.signal(COOKS)
        shared.cook_mutex.unlock()


def main():
    shared = Shared()
    cooks = [Thread(cook, shared, i) for i in range(COOKS)]
    savages = [Thread(savage, shared, i) for i in range(SAVAGES)]

    for t in cooks + savages:
        t.join()


if __name__ == "__main__":
    main()
