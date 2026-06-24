#1 example

numbers = [10, 20, 30]

print(len(numbers))

#2 example

numbers = [10, 20, 30]

print(sum(numbers))

#3 example

numbers = [10, 20, 30]

print(min(numbers))

#4 example

numbers = [10, 20, 30]

print(max(numbers))

#5 example

numbers = [1, 2, 3]

result = list(map(lambda x: x * 2, numbers))

print(result)

#6 example

numbers = [1, 2, 3, 4, 5]

result = list(filter(lambda x: x % 2 == 0, numbers))

print(result)

#7 example

from functools import reduce

numbers = [1, 2, 3, 4]

result = reduce(lambda x, y: x + y, numbers)

print(result)

#8 example

fruits = ["apple", "banana", "orange"]

for index, fruit in enumerate(fruits):
    print(index, fruit)

#9 example

names = ["Ali", "Dana", "Tom"]
scores = [90, 85, 95]

for name, score in zip(names, scores):
    print(name, score)

#10 example

numbers = [5, 2, 8, 1]

print(sorted(numbers))

#11 example

x = "123"

print(int(x))

#12 example
x = "12.5"

print(float(x))

#13 example
x = 123

print(str(x))

#14 example
text = "hello"

print(list(text))