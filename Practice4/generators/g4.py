a = int(input())
b = int(input())

def sqr_gen(a, b):
    for i in range(a, b + 1):
        yield i * i

for x in sqr_gen(a, b):
    print(x)