#1 example

with open("sample.txt", "r") as file:
    print(file.read())

#2 example

with open("sample.txt", "a") as file:
    file.write("\nBonus")

#3 example

with open("sample.txt", "w") as file:
    file.write("Venom")

#4 example

with open("sample.txt", "x") as file:
    file.write("New venom")