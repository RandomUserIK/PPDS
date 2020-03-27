from fei.ppds import Thread, Mutex, Semaphore, print

from random import randint
from time import sleep


class Shared:
    def __init__(self, n):
        self.n = n
        self.customers = 0
        self.standingMutex = Mutex()
        self.sofaMutex = Mutex()
        self.sittingQueue = []
        self.standingQueue = []
        self.standingCustomer = Semaphore(0)
        self.sittingCustomer = Semaphore(0)
        self.sofa = Semaphore(4)
        self.payment = Semaphore(0)
        self.receipt = Semaphore(0)
        self.barber = Semaphore(0)


def accept_payment(barber_id):
    sleep(randint(25, 100) / 100)
    print(f'Barber {barber_id}: accepting a payment.')


def give_receipt(barber_id):
    sleep(randint(25, 100) / 100)
    print(f'Barber {barber_id}: giving a receipt.')


def cut_hair(barber_id):
    sleep(randint(50, 150)/100)
    print(f'Barber {barber_id}: giving a haircut.')


def pay(customer_id):
    sleep(randint(25, 100) / 100)
    print(f'Customer {customer_id}: paying for a haircut.')


def get_hair_cut(customer_id):
    sleep(randint(50, 150)/100)
    print(f'Customer {customer_id}: getting a haircut.')


def sit_on_sofa(customer_id):
    sleep(randint(25, 100) / 100)
    print(f'Customer {customer_id}: sitting on a sofa.')


def sit_in_barber_chair(customer_id):
    sleep(randint(75, 100) / 100)
    print(f'Customer {customer_id}: sitting in the barber chair.')


def enter_shop(customer_id):
    sleep(randint(50, 100) / 100)
    print(f'Customer {customer_id}: entering the barbershop.')


def wait_for_hair_to_grow(customer_id):
    print(f'Customer {customer_id}: waiting for hair to grow.')
    sleep(randint(250, 450) / 100)


def balk(customer_id):
    print(f'Customer {customer_id}: leaving the barbershop...')


def customer(shared, customer_id):
    standing = Semaphore(0)
    sitting = Semaphore(0)

    while True:
        shared.standingMutex.lock()
        if shared.customers == shared.n:
            balk(customer_id)
            shared.standingMutex.unlock()
            continue
        else:
            shared.customers += 1
            shared.standingQueue.append(standing)
            shared.standingMutex.unlock()

        enter_shop(customer_id)
        shared.standingCustomer.signal()
        standing.wait()

        shared.sofa.wait()
        sit_on_sofa(customer_id)
        standing.signal()

        shared.sofaMutex.lock()
        shared.sittingQueue.append(sitting)
        shared.sofaMutex.unlock()

        shared.sittingCustomer.signal()
        sitting.wait()

        sit_in_barber_chair(customer_id)

        shared.barber.wait()
        get_hair_cut(customer_id)

        shared.payment.signal()
        pay(customer_id)
        shared.receipt.wait()

        shared.standingMutex.lock()
        shared.customers -= 1
        shared.standingMutex.unlock()


def barber(shared, barber_id):
    while True:
        shared.standingCustomer.wait()

        shared.standingMutex.lock()
        standing_customer = shared.standingQueue.pop(0)
        standing_customer.signal()
        standing_customer.wait()
        shared.standingMutex.unlock()

        standing_customer.signal()

        shared.sittingCustomer.wait()
        shared.sofaMutex.lock()
        sitting_customer = shared.sittingQueue.pop(0)
        sitting_customer.signal()
        shared.sofaMutex.unlock()

        shared.barber.signal()
        cut_hair(barber_id)

        shared.payment.wait()
        accept_payment(barber_id)
        shared.receipt.signal()


def main():
    shared = Shared(20)
    customers = [Thread(customer, shared, i) for i in range(1, 21)]
    barbers = [Thread(barber, shared, i) for i in range(1, 4)]
    for t in customers + barbers:
        t.join()


if __name__ == "__main__":
    main()
