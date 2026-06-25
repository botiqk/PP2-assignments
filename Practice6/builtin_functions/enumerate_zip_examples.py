#paired iteration

fruits = ["apple", "banana", "orange"]

for index, fruit in enumerate(fruits):
    print(index, fruit)

names = ["Daulet", "Anel", "Almat"]
scores = [67, 86, 73]

for name, score in zip(names, scores):
    print(name, score)
