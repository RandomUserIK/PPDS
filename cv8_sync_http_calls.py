import queue
import time
import urllib.request


def task(name, work_queue):
    while not work_queue.empty():
        url = work_queue.get()
        print(f"Task {name} getting URL: {url}")

        time_start = time.perf_counter()
        urllib.request.urlopen(url)
        elapsed = time.perf_counter() - time_start

        print(f"Task {name} elapsed time: {elapsed:.1f}")
        yield


def main():
    work_queue = queue.Queue()

    for url in [
        "http://google.com",
        "http://yahoo.com",
        "http://linkedin.com",
        "http://apple.com",
        "http://microsoft.com",
        "http://facebook.com",
        "http://twitter.com",

    ]:
        work_queue.put(url)

    tasks = [task('One', work_queue), task('Two', work_queue)]

    done = False
    start_time = time.perf_counter()
    while not done:
        for t in tasks:
            try:
                next(t)
            except StopIteration:
                tasks.remove(t)

            if len(tasks) == 0:
                done = True

    end_time = time.perf_counter() - start_time

    print(f'\nTotal elapsed time: {end_time:.1f}')


if __name__ == '__main__':
    main()
