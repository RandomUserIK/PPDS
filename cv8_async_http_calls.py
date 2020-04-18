import asyncio
import aiohttp
import time


async def task(name, work_queue):
    async with aiohttp.ClientSession() as session:
        while not work_queue.empty():
            url = await work_queue.get()
            print(f'Task {name} getting url: {url}.')
            time_start = time.perf_counter()
            async with session.get(url) as response:
                await response.text()
            elapsed = time.perf_counter() - time_start
            print(f'Task {name} done. Elapsed: {elapsed:.1f}')
            yield


async def main():
    work_queue = asyncio.Queue()

    for url in [
        'http://google.com',
        'http://microsoft.com',
        'http://facebook.com',
        'http://uim.fei.stuba.sk',
        'http://twitter.com',
        'http://apple.com',
        'http://github.com'
    ]:
        await work_queue.put(url)

    time_start = time.perf_counter()
    await asyncio.gather(
        task('One', work_queue),
        task('Two', work_queue)
    )
    elapsed = time.perf_counter() - time_start
    print(f'\nTotal elapsed: {elapsed:.1f}')


if __name__ == '__main__':
    main()
