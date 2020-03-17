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

# Smokers problem solution
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


def main():
    shared = Shared2()

    smokers = []
    agents = []
    pushers = []

    smokers.append(Thread(smoker_matches2, shared))
    smokers.append(Thread(smoker_paper2, shared))
    smokers.append(Thread(smoker_tobacco2, shared))

    agents.append(Thread(agent_1, shared))
    agents.append(Thread(agent_2, shared))
    agents.append(Thread(agent_3, shared))

    pushers.append(Thread(pusher_waiting_matches, shared))
    pushers.append(Thread(pusher_waiting_paper, shared))
    pushers.append(Thread(pusher_waiting_tobacco, shared))

    for thread in smokers + agents + pushers:
        thread.join()


if __name__ == "__main__":
    main()
