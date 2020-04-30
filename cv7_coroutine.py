
def complain_about(substring):
    print('Talk to me.')
    print()

    try:
        while True:
            text = (yield)
            if substring in text:
                print(f'I found {substring} in: {text}.')
    except GeneratorExit:
        print()
        print('Generator Exit raised.')
        print()


def test_generator(substring, text):
    extended_generator = complain_about(substring)

    print(extended_generator)

    # print('calling next...')
    # next(extended_generator)
    extended_generator.send(None)
    extended_generator.send(text)
    extended_generator.close()


def main():
    test_generator('Ruby', 'Hi, Ruby')
    test_generator('World', 'Hello World')
    test_generator('World', 'Hello')


if __name__ == '__main__':
    main()
