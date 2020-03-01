from ppds import Mutex, Thread


class Shared():
    def __init__(self, n):
        self.counter = 0
        self.end = n
        self.elms = [0] * n
        self.mutex = Mutex()


def thread_fnc(shared):
    while True:
        shared.mutex.lock()
        tmp = shared.counter
        shared.counter += 1
        shared.mutex.unlock()
        
        if tmp >= shared.end:
            break
        shared.elms[tmp] += 1 


def histogram(arr):
    return {x: arr.count(x) for x in arr}


shared = Shared(1000000)
t1 = Thread(thread_fnc, shared)
t2 = Thread(thread_fnc, shared)

t1.join()
t2.join()

print(histogram(shared.elms))
