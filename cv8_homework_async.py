import asyncio
import time

import aiohttp

URLS = [
    'http://dsl.sk',
    'http://stuba.sk',
    'http://shmu.sk',
    'http://root.cz',
]


async def request_greetings(work_queue):
    responses = []
    async with aiohttp.ClientSession() as session:
        while not work_queue.empty():
            url = await work_queue.get()

            async with session.get(url) as response:
                response_text = await response.text()
                responses.append(response_text)

    return '\n'.join(responses)


async def main():
    work_queue = asyncio.Queue()

    for url in URLS:
        await work_queue.put(url)

    start_time = time.perf_counter()
    data = await asyncio.gather(
        request_greetings(work_queue),
        request_greetings(work_queue),
        request_greetings(work_queue)
    )
    end_time = time.perf_counter() - start_time

    print(f'Time elapsed: {end_time:.4f}')
    print('\n'.join(data))


if __name__ == '__main__':
    asyncio.run(main())
