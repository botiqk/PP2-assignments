#1 example

with open("sample.txt", "r") as file:
    print(file.read())

#2 example

f = open("sample.txt")
print(f.readline())
f.close()