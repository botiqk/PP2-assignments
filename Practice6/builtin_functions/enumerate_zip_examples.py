#paired iteration

fruits = ["apple", "banana", "orange"]

for index, fruit in enumerate(fruits):
    print(index, fruit)

names = ["Daulet", "Anel", "Almat"]
scores = [67, 86, 73]

for name, score in zip(names, scores):
    print(name, score)

#type checking

x = "123"

print(type(x))

number = int(x)

print(type(number))

y = 12.5

print(int(y))
print(str(y))