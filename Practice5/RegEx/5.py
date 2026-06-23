import re

text = input("Enter text: ")

pattern = r"a.*b%"
if re.search(pattern, text):
    print("Yes")
else:
    print("No")