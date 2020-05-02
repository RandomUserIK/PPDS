import asyncio
import time


async def task(name, work_queue):
    while not work_queue.empty():
        delay = await work_queue.get()
        print(f'Task {name} running.')

        start_time = time.perf_counter()
        await asyncio.sleep(delay)
        end_time = time.perf_counter() - start_time

        print(f'Task {name} elapsed time: {end_time:.1f}')


async def main():
    work_queue = asyncio.Queue()

    for work in [15, 10, 5, 2]:
        await work_queue.put(work)

    start_time = time.perf_counter()
    await asyncio.gather(
        task('One', work_queue),
        task('Two', work_queue)
    )
    end_time = time.perf_counter() - start_time

    print(f'\nTotal elapsed time: {end_time:.1f}')

if __name__ == '__main__':
    asyncio.run(main())
