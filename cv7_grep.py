import sys


def consumer(func):
    def wrapper(*args, **kwargs):
        gen = func(*args, **kwargs)
        next(gen)
        return gen
    return wrapper


def cat(file, gen):
    for line in file:
        gen.send(line)
    gen.close()


@consumer
def grep(substring, gen):
    try:
        while True:
            line = (yield)
            gen.send(line.count(substring))
    except GeneratorExit:
        gen.close()


@consumer
def counter(substring):
    n = 0
    try:
        while True:
            n += (yield)
    except GeneratorExit:
        return substring, n


def main():
    if not len(sys.argv) == 3:
        sys.exit(-1)

    file = open(sys.argv[2])
    substring = sys.argv[1]

    word_counter_generator = counter(substring)
    # next(word_counter_generator)

    grep_generator = grep(substring, word_counter_generator)
    # next(grep_generator)

    cat(file, grep_generator)

    print()


if __name__ == '__main__':
    main()
