import asyncio
import time


async def task(name, work_queue):
    while not work_queue.empty():
        delay = await work_queue.get()
        print(f'Task {name} is running.')
        time_start = time.perf_counter()
        await asyncio.sleep(delay)
        elapsed = time.perf_counter() - time_start
        print(f'Task {name} done. Elapsed: {elapsed:.1f}')


async def main():
    work_queue = asyncio.Queue()

    for work in [5, 3, 4, 1]:
        await work_queue.put(work)

    time_start = time.perf_counter()
    await asyncio.gather(
        task('One', work_queue),
        task('Two', work_queue)
    )
    elapsed = time.perf_counter() - time_start
    print(f'\nTotal elapsed: {elapsed:.1f}')


if __name__ == '__main__':
    asyncio.run(main())
