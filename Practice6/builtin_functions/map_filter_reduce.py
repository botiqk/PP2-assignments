numbers = [1, 2, 3, 4, 5]

# map
doubled = list(map(lambda x: x * 2, numbers))
print(doubled)

# filter
even = list(filter(lambda x: x % 2 == 0, numbers))
print(even)

#aggregate with reduce

from functools import reduce

numbers = [1, 2, 3, 4, 5]

total = reduce(lambda x, y: x + y, numbers)

print(total)