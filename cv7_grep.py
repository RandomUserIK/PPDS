import sys


def consumer(func):
    def wrapper(*args, **kvargs):
        gen = func(*args, **kvargs)
        next(gen)
        return gen

    return wrapper


def cat(file, generator):
    for line in file:
        generator.send(line)
    generator.close()


# decorator usage:
# @consumer == (grep = consumer(grep))
@consumer
def grep(substring,  generator):
    try:
        while True:
            line = (yield)
            generator.send(line.count(substring))
    except GeneratorExit:
        generator.close()

@consumer
def word_count(substring):
    cnt = 0
    try:
        while True:
            cnt += (yield)
    except GeneratorExit:
        print(substring, cnt, flush=True)

@consumer
def dispatch(greps):
    try:
        while True:
            line = (yield)
            for g in greps:
                g.send(line)
    except GeneratorExit:
        for g in greps:
            g.close()


def main():
    if len(sys.argv) < 3:
        print('usage: grep.py <string> ... <file>')
        sys.exit(-1)

    file = open(sys.argv[-1])
    substrings = sys.argv[1: -1]
    greps = []

    for substring in substrings:
        wc_generator = word_count(substring)
        # next(wc_generator) not needed when decorator used

        grep_generator = grep(substring, wc_generator)
        # next(grep_generator)  not needed when decorator used

        greps.append(grep_generator)

    disp = dispatch(greps)
    # next(disp)
    cat(file, disp)


if __name__ == '__main__':
    main()
