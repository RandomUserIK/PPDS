from fei.ppds import Thread, Mutex, Semaphore, Event, print

from random import randint
from time import sleep


# Naive Smokers problem solution
class Shared:
    def __init__(self):
        self.agentSem = Semaphore(1)
        self.tobacco = Semaphore(0)
        self.paper = Semaphore(0)
        self.matches = Semaphore(0)


def smoke():
    sleep(randint(0, 10)/100)


def make_cigarette():
    sleep(randint(0, 10)/100)


def smoker_matches(shared):
    while True:
        sleep(randint(0, 10)/100)
        shared.tobacco.wait()
        print("tobacco: taken by smoker_matches")
        shared.paper.wait()
        print("smokes: smoker_matches")
        make_cigarette()
        shared.agentSem.signal()
        smoke()


def smoker_tobacco(shared):
    while True:
        sleep(randint(0, 10) / 100)
        shared.paper.wait()
        print("paper: taken by smoker_tobacco")
        shared.matches.wait()
        print("smokes: smoker_tobacco")
        make_cigarette()
        shared.agentSem.signal()
        smoke()


def smoker_paper(shared):
    while True:
        sleep(randint(0, 10) / 100)
        shared.matches.wait()
        print("matches: taken by smoker_paper")
        shared.tobacco.wait()
        print("smokes: smoker_paper")
        make_cigarette()
        shared.agentSem.signal()
        smoke()


def agent_1(shared):
    while True:
        sleep(randint(0, 10) / 100)
        shared.agentSem.wait()
        print("agent: paper, tobacco")
        shared.paper.signal()
        shared.tobacco.signal()


def agent_2(shared):
    while True:
        sleep(randint(0, 10) / 100)
        shared.agentSem.wait()
        print("agent: matches, paper")
        shared.matches.signal()
        shared.paper.signal()


def agent_3(shared):
    while True:
        sleep(randint(0, 10) / 100)
        shared.agentSem.wait()
        print("agent: tobacco, matches")
        shared.tobacco.signal()
        shared.matches.signal()


###########################################################################

# Smokers problem solution #1
class Shared2:
    def __init__(self):
        self.isPaper = False
        self.isMatches = False
        self.isTobacco = False

        self.mutex = Mutex()
        self.agentSem = Semaphore(1)

        self.tobacco = Semaphore(0)
        self.paper = Semaphore(0)
        self.matches = Semaphore(0)

        self.pusherTobacco = Semaphore(0)
        self.pusherPaper = Semaphore(0)
        self.pusherMatches = Semaphore(0)


def pusher_waiting_tobacco(shared):
    while True:
        shared.tobacco.wait()
        shared.mutex.lock()
        if shared.isPaper:
            shared.isPaper = False
            shared.pusherMatches.signal()
        elif shared.isMatches:
            shared.isMatches = False
            shared.pusherPaper.signal()
        else:
            shared.isTobacco = True
        shared.mutex.unlock()


def pusher_waiting_matches(shared):
    while True:
        shared.matches.wait()
        shared.mutex.lock()
        if shared.isPaper:
            shared.isPaper = False
            shared.pusherTobacco.signal()
        elif shared.isTobacco:
            shared.isTobacco = False
            shared.pusherPaper.signal()
        else:
            shared.isMatches = True
        shared.mutex.unlock()


def pusher_waiting_paper(shared):
    while True:
        shared.paper.wait()
        shared.mutex.lock()
        if shared.isTobacco:
            shared.isTobacco = False
            shared.pusherMatches.signal()
        elif shared.isMatches:
            shared.isMatches = False
            shared.pusherTobacco.signal()
        else:
            shared.isPaper = True
        shared.mutex.unlock()


def smoker_matches2(shared):
    while True:
        sleep(randint(0, 10)/100)
        shared.pusherMatches.wait()
        print("smokes: smoker_matches")
        make_cigarette()
        shared.agentSem.signal()
        smoke()


def smoker_tobacco2(shared):
    while True:
        sleep(randint(0, 10) / 100)
        shared.pusherTobacco.wait()
        print("smokes: smoker_tobacco")
        make_cigarette()
        shared.agentSem.signal()
        smoke()


def smoker_paper2(shared):
    while True:
        sleep(randint(0, 10) / 100)
        shared.pusherPaper.wait()
        print("smokes: smoker_paper")
        make_cigarette()
        shared.agentSem.signal()
        smoke()


###########################################################################

# Generalized Smokers problem solution
class Shared3:
    def __init__(self):
        self.isPaper = 0
        self.isMatches = 0
        self.isTobacco = 0

        self.mutex = Mutex()
        self.agentSem = Semaphore(1)

        self.tobacco = Semaphore(0)
        self.paper = Semaphore(0)
        self.matches = Semaphore(0)

        self.pusherTobacco = Semaphore(0)
        self.pusherPaper = Semaphore(0)
        self.pusherMatches = Semaphore(0)


def pusher_waiting_tobacco2(shared):
    while True:
        shared.tobacco.wait()
        shared.mutex.lock()
        if shared.isPaper:
            shared.isPaper -= 1
            shared.pusherMatches.signal()
        elif shared.isMatches:
            shared.isMatches -= 1
            shared.pusherPaper.signal()
        else:
            shared.isTobacco += 1
        shared.mutex.unlock()


def pusher_waiting_matches2(shared):
    while True:
        shared.matches.wait()
        shared.mutex.lock()
        if shared.isPaper:
            shared.isPaper -= 1
            shared.pusherTobacco.signal()
        elif shared.isTobacco:
            shared.isTobacco -= 1
            shared.pusherPaper.signal()
        else:
            shared.isMatches += 1
        shared.mutex.unlock()


def pusher_waiting_paper2(shared):
    while True:
        shared.paper.wait()
        shared.mutex.lock()
        if shared.isTobacco:
            shared.isTobacco -= 1
            shared.pusherMatches.signal()
        elif shared.isMatches:
            shared.isMatches -= 1
            shared.pusherTobacco.signal()
        else:
            shared.isPaper += 1
        shared.mutex.unlock()


# def main():
#     shared = Shared3()
#
#     smokers = []
#     agents = []
#     pushers = []
#
#     smokers.append(Thread(smoker_matches2, shared))
#     smokers.append(Thread(smoker_paper2, shared))
#     smokers.append(Thread(smoker_tobacco2, shared))
#
#     agents.append(Thread(agent_1, shared))
#     agents.append(Thread(agent_2, shared))
#     agents.append(Thread(agent_3, shared))
#
#     pushers.append(Thread(pusher_waiting_matches2, shared))
#     pushers.append(Thread(pusher_waiting_paper2, shared))
#     pushers.append(Thread(pusher_waiting_tobacco2, shared))
#
#     for thread in smokers + agents + pushers:
#         thread.join()



# M a N su parametre modelu, nie synchronizaAcie ako takej.
# Preto ich nedavame do zdielaneho objektu.
# M - pocet porcii misionara, ktore sa zmestia do hrnca.
# N - pocet divochov v kmeni (kuchara nepocitame).
M = 2
N = 3
K = 3


class SimpleBarrier:
    """Vlastna implementacia bariery
    kvoli specialnym vypisom vo funkcii wait().
    """
    def __init__(self, N):
        self.N = N
        self.mutex = Mutex()
        self.cnt = 0
        self.sem = Semaphore(0)

    def wait(self,
             print_str,
             savage_id,
             print_last_thread=False,
             print_each_thread=False):
        self.mutex.lock()
        self.cnt += 1
        if print_each_thread:
            print(print_str % (savage_id, self.cnt))
        if self.cnt == self.N:
            self.cnt = 0
            if print_last_thread:
                print(print_str % (savage_id))
            self.sem.signal(self.N)
        self.mutex.unlock()
        self.sem.wait()


# V tomto pripade musime pouzit zdielanu strukturu.
# Kedze Python struktury nema, pouzijeme triedu bez vlastnych metod.
# Preco musime pouzit strukturu? Lebo chceme zdielat hodnotu
# pocitadla servings, a to jednoduchsie v Pythone asi neurobime.
# Okrem toho je rozumne mat vsetky synchronizacne objekty spolu.
# Pri zmene nemusime upravovat API kazdej funkcie zvlast.
class Shared:
    def __init__(self):
        self.mutex = Mutex()
        self.cook_mutex = Mutex()
        self.servings = 0
        self.num_cooks = 0
        self.full_pot = Semaphore(0)
        self.empty_pot = Semaphore(0)
        self.cooks = Semaphore(0)
        self.barrier1 = SimpleBarrier(N)
        self.barrier2 = SimpleBarrier(N)


# Pristupujeme ku zdielanej premennej.
# Preco nie je vo funkcii zamknutie mutexu?!
def get_serving_from_pot(savage_id, shared):
    print("divoch %2d: beriem si porciu" % savage_id)
    shared.servings -= 1


def eat(savage_id):
    print("divoch %2d: hodujem" % savage_id)
    # Zjedenie porcie misionara nieco trva...
    sleep(0.2 + randint(0, 3) / 10)


def savage(savage_id, shared):
    while True:
        # Nasleduje klasicke riesenie problemu hodujucich divochov.
        shared.mutex.lock()
        print("divoch %2d: pocet zostavajucich porcii v hrnci je %2d" %
              (savage_id, shared.servings))
        if shared.servings == 0:
            print("divoch %2d: budim kuchara" % savage_id)
            shared.cooks.signal(K)
            shared.full_pot.wait()
        get_serving_from_pot(savage_id, shared)
        shared.mutex.unlock()

        eat(savage_id)


def put_servings_in_pot(M, shared):
    """M je pocet porcii, ktore vklada kuchar do hrnca.
    Hrniec je reprezentovany zdielanou premennou servings.
    Ta udrziava informaciu o tom, kolko porcii je v hrnci k dispozicii.
    """
    print("kuchar: varim")
    # navarenie jedla tiez cosi trva...
    sleep(0.4 + randint(0, 2) / 10)
    shared.servings += 1


def cook(M, shared, cook_id):
    """Na strane kuchara netreba robit ziadne modifikacie kodu.
    Riesenie je standardne podla prednasky.
    Navyse je iba argument M, ktorym explicitne hovorime, kolko porcii
    ktory kuchar vari.
    Kedze v nasom modeli mame iba jedneho kuchara, ten navari vsetky
    potrebne porcie a vlozi ich do hrnca.
    """
    while True:

        shared.cooks.wait()

        shared.barrier1.wait(
            "cook %2d: prisiel som ku kotlu, uz nas je %2d",
            cook_id,
            print_each_thread=True)

        shared.cook_mutex.lock()

        print("cook %2d: pocet porcii v hrnci je %2d" %
              (cook_id, shared.servings))

        shared.num_cooks += 1

        if not shared.servings == M:
            put_servings_in_pot(M, shared)

        if shared.num_cooks == K:
            if shared.servings == M:
                print("cook %2d: budim divochov" % cook_id)
                shared.full_pot.signal()
                shared.num_cooks = 0
            else:
                shared.num_cooks = 0
                shared.cooks.signal(K)

        shared.cook_mutex.unlock()

        shared.barrier2.wait("cook %2d: uz sme vsetci, zaciname varit",
                             cook_id,
                             print_last_thread=True)


# Spustenie modelu.


def init_and_run(N, M):
    threads = list()
    shared = Shared()
    for savage_id in range(0, N):
        threads.append(Thread(savage, savage_id, shared))

    for cook_id in range(0, K):
        threads.append(Thread(cook, M, shared, cook_id))

    for t in threads:
        t.join()


if __name__ == "__main__":
    init_and_run(N, M)

