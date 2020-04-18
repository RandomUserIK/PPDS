def complain_about(substring):
    print('Please talk to me!')

    try:
        while True:
            text = (yield)
            if substring in text:
                print(f'Oh no: I found {substring} in: {text}.')
    except GeneratorExit:
        print()
        print('GeneratorExit raised. Ok, ok: I am quitting.')
        print()


c = complain_about('Ruby')
print(c)

# next(c) # init
c.send(None)  # init
c.send('Hi, Ruby')
c.send('Hello World')
c.send('Hi, it\'s Ruby again')
c.close()
