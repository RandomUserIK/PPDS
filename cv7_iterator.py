class MyIterator:
    def __init__(self, n):
        self.n = n

    def __iter__(self):
        return self

    def __next__(self):
        if self.n:
            return self.n.pop(0)
        raise StopIteration


def test1_my_iterator(text):
    print(f'(text):')
    print('-' * (len(text) + 1))

    print(MyIterator([0, 1, 2]))

    it = MyIterator([1, 2])
    try:
        print(next(it))
        print(next(it))
        print(next(it))
    except StopIteration:
        print('Stop Iteration raised.')

    for i in MyIterator([0, 1, 2]):
        print(i)
    print()


def test2_my_iterator(text):
    print(f'{text}:')
    print('-' * (len(text) + 1))

    it = MyIterator([3, 4, 5, 6])
    print(it)

    print(next(it))
    print(next(it))
    print(next(it))
    print(next(it))

    try:
        print(next(it))
    except StopIteration:
        print('StopIteration raised')


def main():
    test1_my_iterator('test 1')
    test2_my_iterator('test 2')


if __name__ == "__main__":
    main()
