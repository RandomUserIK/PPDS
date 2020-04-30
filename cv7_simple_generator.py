def simple_generator(n):
    while n:
        n -= 1
        yield n


def test_generator():
    generator = simple_generator(3)

    print(generator)

    try:
        print(next(generator))
        print(next(generator))
        print(next(generator))
        print(next(generator))
    except StopIteration:
        print('Stop Iteration raised.')
        print()

    print(x for x in range(10))
    print(list(x for x in range(10)))


def main():
    test_generator()


if __name__ == "__main__":
    main()
