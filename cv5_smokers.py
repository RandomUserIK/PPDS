from random import randint
from time import sleep

from fei.ppds import Thread, Mutex, Semaphore, print


class Shared:
    def __init__(self):
        self.num_tobacco = 0
        self.num_paper = 0
        self.num_matches = 0

        self.mutex = Mutex()

        self.agent_sem = Semaphore(1)

        self.tobacco = Semaphore(0)
        self.paper = Semaphore(0)
        self.matches = Semaphore(0)

        self.tobacco_pusher = Semaphore(0)
        self.paper_pusher = Semaphore(0)
        self.matches_pusher = Semaphore(0)


def agent_1(shared):
    while True:
        shared.agent_sem.wait()
        print('Agent: matches.')
        shared.tobacco_pusher.signal()
        shared.paper_pusher.signal()


def agent_2(shared):
    while True:
        shared.agent_sem.wait()
        print('Agent: tobacco.')
        shared.matches_pusher.signal()
        shared.paper_pusher.signal()


def agent_3(shared):
    while True:
        shared.agent_sem.wait()
        print('Agent: paper.')
        shared.tobacco_pusher.signal()
        shared.matches_pusher.signal()


def pusher_tobacco(shared):
    while True:
        shared.tobacco_pusher.wait()
        print('Tobacco pusher.')
        shared.mutex.lock()
        if shared.num_matches > 0:
            shared.num_matches -= 1
            shared.paper.signal()
        elif shared.num_paper > 0:
            shared.num_paper -= 1
            shared.matches.signal()
        else:
            shared.num_tobacco += 1
        shared.mutex.unlock()


def pusher_paper(shared):
    while True:
        shared.paper_pusher.wait()
        print('Paper pusher.')
        shared.mutex.lock()
        if shared.num_matches > 0:
            shared.num_matches -= 1
            shared.tobacco.signal()
        elif shared.num_tobacco > 0:
            shared.num_tobacco -= 1
            shared.matches.signal()
        else:
            shared.num_paper += 1
        shared.mutex.unlock()


def pusher_matches(shared):
    while True:
        shared.matches_pusher.wait()
        print('Matches pusher.')
        shared.mutex.lock()
        if shared.num_tobacco > 0:
            shared.num_tobacco -= 1
            shared.paper.signal()
        elif shared.num_paper > 0:
            shared.num_paper -= 1
            shared.matches.signal()
        else:
            shared.num_matches += 1
        shared.mutex.unlock()


def smoker_tobacco(shared):
    while True:
        shared.tobacco.wait()
        make_cigarette('smoker_tobacco')
        shared.agent_sem.signal()
        smoke('smoker_tobacco')


def smoker_matches(shared):
    while True:
        shared.matches.wait()
        make_cigarette('smoker_matches')
        shared.agent_sem.signal()
        smoke('smoker_matches')


def smoker_paper(shared):
    while True:
        shared.paper.wait()
        make_cigarette('smoker_paper')
        shared.agent_sem.signal()
        smoke('smoker_paper')


def smoke(smoker_id):
    print(f'Smoker {smoker_id}: smoking.')
    sleep(randint(0, 10) / 10)


def make_cigarette(smoker_id):
    print(f'Smoker {smoker_id}: making a cigarette.')
    sleep(randint(0, 10) / 10)


def main():
    shared = Shared()
    agents = []
    smokers = []
    pushers = []

    agents.append(Thread(agent_1, shared))
    agents.append(Thread(agent_2, shared))
    agents.append(Thread(agent_3, shared))

    pushers.append(Thread(pusher_matches, shared))
    pushers.append(Thread(pusher_tobacco, shared))
    pushers.append(Thread(pusher_paper, shared))

    smokers.append(Thread(smoker_matches, shared))
    smokers.append(Thread(smoker_paper, shared))
    smokers.append(Thread(smoker_tobacco, shared))

    for t in agents + smokers:
        t.join()


if __name__ == "__main__":
    main()