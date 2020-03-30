from random import randint
from time import sleep

from fei.ppds import Thread, Semaphore, print


class Shared:
    def __init__(self):
        self.agent_sem = Semaphore(1)

        self.tobacco = Semaphore(0)
        self.paper = Semaphore(0)
        self.matches = Semaphore(0)


def agent_1(shared):
    while True:
        shared.agent_sem.wait()
        print('Agent: tobacco, paper.')
        shared.tobacco.signal()
        shared.paper.signal()


def agent_2(shared):
    while True:
        shared.agent_sem.wait()
        print('Agent: matches, paper.')
        shared.matches.signal()
        shared.paper.signal()


def agent_3(shared):
    while True:
        shared.agent_sem.wait()
        print('Agent: paper, matches.')
        shared.paper.signal()
        shared.matches.signal()


def smoker_tobacco(shared):
    while True:
        print('Smoker: tobacco')
        shared.paper.wait()
        shared.matches.wait()
        make_cigarette('smoker_tobacco')
        smoke('smoker_tobacco')
        shared.agent_sem.signal()


def smoker_matches(shared):
    while True:
        print('Smoker: matches')
        shared.paper.wait()
        shared.tobacco.wait()
        make_cigarette('smoker_matches')
        smoke('smoker_matches')
        shared.agent_sem.signal()


def smoker_paper(shared):
    while True:
        print('Smoker: paper')
        shared.tobacco.wait()
        shared.matches.wait()
        make_cigarette('smoker_paper')
        smoke('smoker_paper')
        shared.agent_sem.signal()


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

    agents.append(Thread(agent_1, shared))
    agents.append(Thread(agent_2, shared))
    agents.append(Thread(agent_3, shared))

    smokers.append(Thread(smoker_matches, shared))
    smokers.append(Thread(smoker_paper, shared))
    smokers.append(Thread(smoker_tobacco, shared))

    for t in agents + smokers:
        t.join()


if __name__ == "__main__":
    main()