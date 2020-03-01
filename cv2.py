from ppds import Mutex, Event, Semaphore, Thread
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
""" class SimpleBarrier():
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
""" class Shared():
    def __init__(self, N):
        self.N = N
        self.count = 0
        self.mutex = Mutex()
        self.semaphore = Semaphore(0)


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
        ko(thread_id)


def barrier_example(shared, thread_id):
    sleep(randint(1,10)/10)
    print("vlakno %s pred barierou" % thread_id)
    barrier(shared, thread_id)
    print("vlakno %s po bariere" % thread_id) 


simpleBarrier = SimpleBarrier(10)
shared = Shared(10)

threads = list()
for i in range(10):
    thread_id = 'Thread ' + str(i)
    t = Thread(barrier_example, shared, thread_id)
    threads.append(t)
 
for t in threads:
    t.join()  """


# Task 3 - Fibonacci
class Shared():
    def __init__(self, N):
        self.N = N
        self.count = 0 
        self.mutex = Mutex()
        self.semaphore = Semaphore(0)
        self.arr = [0, 1] + [0] * N
    
def fibonacci(N):
    return fibonacci(N - 1) + fibonacci(N - 2)
