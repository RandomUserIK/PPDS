import aiohttp
import asyncio
import time


async def task(name, work_queue):
    async with aiohttp.ClientSession() as session:
        while not work_queue.empty():
            url = await work_queue.get()
            print(f'Task {name} getting URL: {url}')

            start_time = time.perf_counter()
            async with session.get(url) as response:
                await response.text()
            end_time = time.perf_counter() - start_time

            print(f'Task {name} elapsed time: {end_time:.1f}')


async def main():
    work_queue = asyncio.Queue()

    for url in [
        "http://google.com",
        "http://linkedin.com",
        "http://apple.com",
        "http://microsoft.com",
        "http://facebook.com",
        "http://twitter.com",

    ]:
        await work_queue.put(url)

    start_time = time.perf_counter()
    await asyncio.gather(
        task('One', work_queue),
        task('Three', work_queue),
        task('Four', work_queue),
        task('Five', work_queue),
        task('Six', work_queue),
        task('Seven', work_queue)
    )
    end_time = time.perf_counter() - start_time

    print(f'\nTotal time elapsed: {end_time:.1f}')


if __name__ == '__main__':
    asyncio.run(main())
