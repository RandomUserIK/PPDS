from fei.ppds import Mutex, Event, Semaphore, Thread
from random import randint
from time import sleep

def rendezvous(thread_id):
    sleep(randint(1,10)/10)
    print('rendezvous: %s' % thread_id)
 

def ko(thread_id):
    print('ko: %s' % thread_id)
    sleep(randint(1,10)/10)


""" def barrier_example(barrier, thread_id):
    sleep(randint(1,10)/10)
    print("vlakno %s pred barierou" % thread_id)
    barrier.barrier(thread_id)
    print("vlakno %s po bariere" % thread_id) """


# Task 1 - preloaded Turnstile
""" class SimpleBarrier:
    def __init__(self, N):
        self.N = N
        self.semaphore = Semaphore(0)
        self.mutex = Mutex()
        self.count = 0
    
    def barrier(self, thread_name):
        rendezvous(thread_name)
        self.mutex.lock()
        self.count += 1
        if self.count == self.N:
            self.count = 0 
            self.semaphore.signal(self.N)
        self.mutex.unlock()
        print("vlakno %s na semafore" % thread_id)
        self.semaphore.wait()
        ko(thread_name) """


# Task 2 - simple barrier
""" class Shared:
    def __init__(self, N):
        self.N = N
        self.count = 0
        self.mutex = Mutex()
        self.semaphore = Semaphore(0)
        self.event = Event()


def barrier(shared, thread_id):
        rendezvous(thread_id)
        shared.mutex.lock()
        shared.count += 1
        if shared.count == shared.N:
            shared.semaphore.signal()
        shared.mutex.unlock()
        print("vlakno %s na semafore" % thread_id)
        shared.semaphore.wait()
        shared.semaphore.signal()
        ko(thread_id) """ 


# Barrier with Event
# Soulution 1 - not optimal (two serializations needed)
""" def barrier_event1(shared, thread_id):
    rendezvous(thread_id)

    shared.mutex.lock()
    shared.count += 1
    if shared.count == shared.N:
        shared.event.set()
    shared.mutex.unlock()

    print("vlakno %s na semafore" % thread_id)
    shared.event.wait()
    ko(thread_id)
    # shared.event.clear() last thread must call for clear

    shared.mutex.lock()
    shared.count -= 1
    if shared.count == 0:
        shared.event.clear()
    shared.mutex.unlock()


# Soulution 2 
def barrier_event2(shared, thread_id):
    rendezvous(thread_id)

    shared.mutex.lock()
    if shared.count == 0:
        shared.event.clear()

    shared.count += 1

    if shared.count == shared.N:
        shared.event.set()
    shared.mutex.unlock()

    print("vlakno %s na semafore" % thread_id)
    shared.event.wait()
    ko(thread_id)


def barrier_example(shared, thread_id):
    sleep(randint(1,10)/10)
    print("vlakno %s pred barierou" % thread_id)
    barrier_event2(shared, thread_id)
    print("vlakno %s po bariere" % thread_id) 


# simpleBarrier = SimpleBarrier(10)
shared = Shared(10)

threads = list()
for i in range(10):
    thread_id = 'Thread ' + str(i)
    t = Thread(barrier_example, shared, thread_id)
    threads.append(t)
 
for t in threads:
    t.join()   """


# Task 3 - Fibonacci
# Version 1
""" class Shared():
    def __init__(self, N):
        self.N = N
        self.fib_seq = [0, 1] + [0] * N
        self.semaphores = [Semaphore(0) for i in range(N + 2)]
        self.semaphores[0].signal(2)
        self.semaphores[1].signal(1) 

def thread_function(shared, thread_id):
    sleep(randint(0,10)/10)
    
    print("Thread %d: start" % thread_id)
    shared.semaphores[thread_id].wait()
    shared.semaphores[thread_id].wait()

    print("Thread %d: continues" % thread_id)
    fibonacci(shared.fib_seq, thread_id)

    shared.semaphores[thread_id + 1].signal()
    shared.semaphores[thread_id + 2].signal()
    print("Thread %d: stop" % thread_id) """


# Version 2
class Shared:
    def __init__(self, N):
        self.N = N
        self.fib_seq = [0, 1] + [0] * N
        self.semaphores = [Semaphore(0) for i in range(N + 1)]
        self.semaphores[0].signal(1)


def fibonacci(fib_seq, thread_id):
    fib_seq[thread_id + 2] = fib_seq[thread_id] + fib_seq[thread_id + 1]


def thread_function(shared, thread_id):
    sleep(randint(0,10)/10)

    print("Thread %d: start" % thread_id)
    shared.semaphores[thread_id].wait()

    print("Thread %d: continues" % thread_id)
    fibonacci(shared.fib_seq, thread_id)

    shared.semaphores[thread_id + 1].signal()
    print("Thread %d: stop" % thread_id)


shared = Shared(10)
threads = []

for i in range(shared.N):
    threads.append(Thread(thread_function, shared, i))

for thread in threads:
    thread.join()

print("\nFibonacci sequence:")
for ind, val in enumerate(shared.fib_seq):
    print(ind, val, sep=": ")