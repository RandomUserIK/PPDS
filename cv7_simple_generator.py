def my_generator(n):
    while n:
        n -= 1
        yield n


g = my_generator(3)
print(g)
print(next(g))
print(next(g))
print(next(g))

try:
    print(next(g))
except StopIteration:
    print('StopIteration raised in my_generator')


for i in my_generator(4):
    print(i)