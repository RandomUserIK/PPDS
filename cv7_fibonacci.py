class Fibonacci:
    def __init__(self, limit):
        self.a = 0
        self.b = 1
        self.i = 1
        self.limit = limit

    def __iter__(self):
        return self

    def __next__(self):
        if self.i > self.limit:
            raise StopIteration

        if self.i > 1:
            self.a, self.b = self.b, self.a + self.b

        self.i += 1
        return self.b


def fib(limit):
    i = 1
    a, b = 0, 1

    while True:
        if i > limit:
            raise GeneratorExit
        yield b
        a, b = b, a + b
        i += 1


######################################

f = Fibonacci(10)
print(dir(f))
print(f)

print(next(f))
print(next(f))
print(next(f))

for i in f:
    print(i)

######################################

b = fib(10)
print(b)
print(dir(b))

print(next(b))
print(next(b))
print(next(b))

for i in b:
    print(i)
