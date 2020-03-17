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


def main():
    shared = Shared()

    smokers = []
    agents = []

    smokers.append(Thread(smoker_matches, shared))
    smokers.append(Thread(smoker_paper, shared))
    smokers.append(Thread(smoker_tobacco, shared))

    agents.append(Thread(agent_1, shared))
    agents.append(Thread(agent_2, shared))
    agents.append(Thread(agent_3, shared))

    for thread in smokers + agents:
        thread.join()


if __name__ == "__main__":
    main()
