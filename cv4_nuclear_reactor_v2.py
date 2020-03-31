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
        self.t_done = False
        self.p_done = False
        self.h_done = False


def get_writing_duration(shared, cidlo_id):
    if cidlo_id == 'P':
        shared.p_done = True
        return randint(10, 20)
    elif cidlo_id == 'T':
        shared.t_done = True
        return randint(10, 20)
    else:
        shared.h_done = True
        return randint(20, 25)


def cidlo(shared, cidlo_id):
    while True:
        sleep(randint(50, 60) / 1000)
        shared.turnstile.wait()
        num_waiting_cidla = shared.ls_cidlo.lock(shared.access_data)
        shared.turnstile.signal()

        writing_duration = get_writing_duration(shared, cidlo_id)
        print(f'Cidlo {cidlo_id}, number of waiting cidiel: {num_waiting_cidla}, writing duration: {writing_duration}')
        sleep(writing_duration / 1000)

        shared.ls_cidlo.unlock(shared.access_data)

        if shared.p_done and shared.t_done and shared.h_done:
            shared.valid_data.set()


def monitor(shared, monitor_id):
    shared.valid_data.wait()

    while True:
        shared.turnstile.wait()
        shared.turnstile.signal()

        num_waiting_monitors = shared.ls_monitor.lock(shared.access_data)

        print(f'Monitor {monitor_id}: number of waiting monitors: {num_waiting_monitors}')

        sleep(randint(40, 50) / 1000)
        shared.ls_monitor.unlock(shared.access_data)


def main():
    shared = Shared()
    [Thread(monitor, shared, i) for i in range(8)]
    Thread(cidlo, shared, 'P')
    Thread(cidlo, shared, 'H')
    Thread(cidlo, shared, 'T')



if __name__ == "__main__":
    main()