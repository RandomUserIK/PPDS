import queue
import urllib.request
import time


def task(name, work_queue):
    while not work_queue.empty():
        url = work_queue.get()
        print(f'Task {name} getting url: {url}.')
        time_start = time.perf_counter()
        urllib.request.urlopen(url)
        elapsed = time.perf_counter() - time_start
        print(f'Task {name} done. Elapsed: {elapsed:.1f}')
        yield


def main():
    work_queue = queue.Queue()

    for url in [
        'http://google.com',
        'http://microsoft.com',
        'http://facebook.com',
        'http://uim.fei.stuba.sk',
        'http://twitter.com',
        'http://apple.com',
        'http://github.com'
    ]:
        work_queue.put(url)

    tasks = [
        task('One', work_queue),
        task('Two', work_queue)
    ]

    done = False
    time_start = time.perf_counter()
    while not done:
        for t in tasks:
            try:
                next(t)
            except StopIteration:
                tasks.remove(t)
            if not tasks:
                done = True
    elapsed = time.perf_counter() - time_start
    print(f'\nTotal elapsed: {elapsed:.1f}')


if __name__ == '__main__':
    main()
