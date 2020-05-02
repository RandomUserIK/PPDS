from urllib.request import urlopen
import time

URLS = [
    'http://dsl.sk',
    'http://stuba.sk',
    'http://shmu.sk',
    'http://root.cz',
]


def request_greetings():
    responses = []
    for url in URLS:
        resp = urlopen(url)
        responses.append(resp.read().decode('latin-1'))
    texts = '\n'.join(responses)
    return texts


if __name__ == "__main__":
    t1 = time.time()
    greetings = request_greetings()
    print(time.time() - t1, "seconds passed")
    print(greetings)