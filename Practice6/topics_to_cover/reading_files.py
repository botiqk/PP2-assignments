#1 example

f = open("sample.txt")
print(f.read())

#2 example

with open("sample.txt") as f:
  print(f.readline())

#3 example

with open("sample.txt") as f:
  print(f.readlines())