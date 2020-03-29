from fei.ppds import Thread, Mutex, Semaphore, print


class Shared:
    def __init__(self):
        self.mutex = Mutex()
        self.room1 = 0
        self.room2 = 0
        self.turnstile1 = Semaphore(1)  # weak semaphores
        self.turnstile2 = Semaphore(1)


def thread_func(shared, thread_id):
    while True:
        # as thread enters room 1, we increment the number of threads in room 1
        shared.mutex.lock()
        shared.room1 += 1
        shared.mutex.unlock()

        shared.turnstile1.wait()
        # threads pass the turnstile one by one, hence mutex protection is not needed here
        shared.room2 += 1

        # mutex is needed here because another thread might increment the room 1 counter on line 20
        shared.mutex.lock()
        shared.room1 -= 1

        if shared.room1 == 0:
            shared.turnstile2.signal()  # if all threads have left the room 1, let the waiting threads enter room 2
            shared.mutex.unlock()
        else:
            shared.turnstile1.signal()  # otherwise, let a random waiting thread pass from room 1 to room 2
            shared.mutex.unlock()

        shared.turnstile2.wait()
        # threads pass again one by one
        # no need for mutex since line 25 is not reachable now, we already know for sure that the room 1 is empty
        shared.room2 -= 1

        # critical section

        if shared.room2 == 0:
            shared.turnstile1.signal()  # if all threads have left the room 2, let the waiting threads enter room 1
        else:
            shared.turnstile2.signal()  # otherwise, let a random waiting thread pass from room 2 to room 1


def main():
    pass


if __name__ == "__main__":
    main()