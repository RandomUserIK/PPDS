from random import randint
from time import sleep

from fei.ppds import Thread, Mutex, Semaphore, print


# nemozno pouzit Event - ked je nastavena udalost prechadzaju vsetci
#                      - ked je vynulovana vsetci cakaju
# poziadavka v danej ulohe: PRAVE JEDEN sa ide strihat - pri udalosti toto nie je zarucene
# rozdiel medzi udalostou a semaforom - pri udalosti nevieme urcit, kolkym je doruceny signal
#                                     - pri semafore vieme presne kolkym moze byt doruceny, bez toho aby sa zablokovali
# pri pouziti slabeho semaforu nastane predbiehanie zakaznikov
# vchadzanie do holicstva - konkurentne
# samotna fronta semaforov by nam nestacila, potrebujeme aj pocitadlo
# scoreboard - kolko je obsadenych stoliciek
# 2x rendezvous
# rendezvous nie je implementovane optimalne - mohlo by byt, nepokazi sa program

class Shared:
    def __init__(self, n):
        self.n = n
        self.customers = 0
        self.mutex = Mutex()
        self.customer = Semaphore(0)
        self.customerDone = Semaphore(0)
        self.barber = Semaphore(0)
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
            shared.customers += 1
            shared.mutex.unlock()

        # signal the arrival and wait for the barber
        shared.customer.signal()
        shared.barber.wait()

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
        shared.barber.signal()

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