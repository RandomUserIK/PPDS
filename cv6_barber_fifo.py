from fei.ppds import Thread, Mutex, Semaphore, print

from random import randint
from time import sleep


class Shared:
    def __init__(self, n):
        self.n = n
        self.customers = 0
        self.queue = []  # we want customers to proceed in the order they arrive
        self.mutex = Mutex()
        self.customer = Semaphore(0)
        self.customerDone = Semaphore(0)
        self.barberDone = Semaphore(0)


def balk(customer_id):
    print(f'Customer: {customer_id} leaving the barbershop...')


def get_hair_cut(customer_id):
    sleep(randint(50, 150)/100)
    print(f'Customer: {customer_id} is getting a haircut.')


def cut_hair():
    sleep(randint(50, 150)/100)
    print('Barber giving a haircut.')


def wait_for_hair_to_grow(customer_id):
    print(f'Customer: {customer_id} waiting for hair to grow')
    sleep(randint(250, 450) / 100)


def customer(shared, customer_id):
    barber = Semaphore(0)  # each thread will have its own Semaphore

    while True:
        # wait for hair to grow back
        wait_for_hair_to_grow(customer_id)

        shared.mutex.lock()
        # check if there are available seats
        if shared.customers == shared.n:
            # if there aren't any, leave
            balk(customer_id)
            shared.mutex.unlock()  # if this is omitted - deadlock will occur
            continue
        else:
            # if yes, proceed
            print(f'Customer {customer_id} has arrived and is waiting.')
            shared.queue.append(barber)
            shared.customers += 1
            shared.mutex.unlock()

        # signal the arrival and wait for the barber
        shared.customer.signal()
        barber.wait()

        get_hair_cut(customer_id)

        # signal if haircut is satisfactory
        shared.customerDone.signal()
        shared.barberDone.wait()

        # leave
        shared.mutex.lock()
        shared.customers -= 1
        shared.mutex.unlock()


def barber(shared):
    while True:
        # wait for a customer
        shared.customer.wait()
        shared.mutex.lock()  # because it needs to access the queue
        barber = shared.queue.pop(0)  # first one in line will proceed
        shared.mutex.unlock()

        barber.signal()

        # give a haircut
        cut_hair()

        # wait until haircut is satisfactory
        shared.customerDone.wait()
        shared.barberDone.signal()


def main():
    number_of_customers = 5
    shared = Shared(number_of_customers)
    customers = [Thread(customer, shared, i) for i in range(10)]
    hair_stylist = Thread(barber, shared)

    for t in customers:
        t.join()
    hair_stylist.join()


if __name__ == "__main__":
    main()