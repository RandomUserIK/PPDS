import queue
import time


def task(name, queue):
    while not queue.empty():
        delay = queue.get()
        print(f"Task {name} running")

        time_start = time.perf_counter()
        time.sleep(delay)
        elapsed = time.perf_counter() - time_start

        print(f"Task {name} elapsed time: {elapsed:.1f}")
        yield


def main():
    work_queue = queue.Queue()

    for work in [15, 10, 5, 2]:
        work_queue.put(work)

    tasks = [task("One", work_queue), task("Two", work_queue)]

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
    elapsed = time.perf_counter() - start_time
    print(f"\nTotal elapsed time: {elapsed:.1f}")


if __name__ == "__main__":
    main()
