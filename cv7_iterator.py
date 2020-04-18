class MyIterator(object):
    def __init__(self, xs):
        self.xs = xs

    def __iter__(self):
        return self

    def __next__(self):
        if self.xs:
            return self.xs.pop(0)
        raise StopIteration


def test1_my_iterator(text):
    print(f'(text):')
    print('-' * (len(text) + 1))

    print(MyIterator([0, 1, 2]))
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


if __name__ == '__main__':
    test1_my_iterator('test1')
    test2_my_iterator('test2')
