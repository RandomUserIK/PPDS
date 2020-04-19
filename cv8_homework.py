import asyncio
import aiohttp
import time


URLS = [
    'http://dsl.sk',
    'http://stuba.sk',
    'http://shmu.sk',
    'http://root.cz',
]


async def request_greetings(work_queue) -> str:
    responses = []
    async with aiohttp.ClientSession() as session:
        while not work_queue.empty():
            url = await work_queue.get()
            async with session.get(url) as response:
                resp = await response.text()
                responses.append(resp)
    texts = '\n'.join(responses)
    return texts


async def main():
    work_queue = asyncio.Queue()

    for url in URLS:
        await work_queue.put(url)

    t1 = time.perf_counter()

    greetings = await asyncio.gather(
        request_greetings(work_queue),
        request_greetings(work_queue)
    )

    print(time.perf_counter() - t1, 'seconds passed')
    print('\n'.join(greetings))

if __name__ == "__main__":
    asyncio.run(main())
