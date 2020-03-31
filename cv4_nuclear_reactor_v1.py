from random import randint
from time import sleep

from fei.ppds import Thread, Mutex, Semaphore, Event, print


class Lightswitch:
    def __init__(self):
        self.counter = 0
        self.mutex = Mutex()

    def lock(self, semaphore):
        self.mutex.lock()
        self.counter += 1
        if self.counter == 1:
            semaphore.wait()
        self.mutex.unlock()
        return self.counter

    def unlock(self, semaphore):
        self.mutex.lock()
        self.counter -= 1
        if self.counter == 0:
            semaphore.signal()
        self.mutex.unlock()


class Shared:
    def __init__(self):
        self.access_data = Semaphore(1)
        self.turnstile = Semaphore(1)
        self.ls_monitor = Lightswitch()
        self.ls_cidlo = Lightswitch()
        self.valid_data = Event()


def cidlo(shared, cidlo_id):
    while True:
        shared.turnstile.wait()
        shared.turnstile.signal()

        num_waiting_cidla = shared.ls_cidlo.lock(shared.access_data)

        writing_duration = randint(10, 15)
        print(f'Cidlo {cidlo_id}, number of waiting cidiel: {num_waiting_cidla}, writing duration: {writing_duration}')
        sleep(writing_duration / 1000)

        shared.valid_data.signal()
        shared.ls_cidlo.unlock(shared.access_data)


def monitor(shared, monitor_id):
    shared.valid_data.wait()

    while True:
        sleep(0.5)

        shared.turnstile.wait()
        num_waiting_monitors = shared.ls_monitor.lock(shared.access_data)
        shared.turnstile.signal()

        print(f'Monitor {monitor_id}: number of waiting monitors: {num_waiting_monitors}')

        shared.ls_monitor.unlock(shared.access_data)


def main():
    shared = Shared()
    [Thread(cidlo, shared, i) for i in range(11)]
    [Thread(monitor, shared, i) for i in range(2)]


if __name__ == "__main__":
    main()