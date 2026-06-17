n = int(input())

def desc_gen(x):
    while x >= 0:
        yield x
        x -= 1

for nums in desc_gen(n):
    print(nums)