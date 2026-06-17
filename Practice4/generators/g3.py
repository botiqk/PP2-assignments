n = int(input())

def div_gen(n):
    for i in range(n + 1):
        if i % 3 == 0 and i % 4 == 0:
            yield i

for div in div_gen(n):
    print(div)