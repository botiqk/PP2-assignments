with open("sample.txt", "a") as f:
    f.write("\nVenom")

with open("sample.txt", "r") as f:
    print(f.read())