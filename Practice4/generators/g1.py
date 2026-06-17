n = int(input())
square = (x * x for x in range(n + 1))

for x in square:
    print(x)