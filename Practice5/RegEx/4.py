import re

text = input("Enter text: ")

pattern = r"[A-Z][a-z]+"
res = re.findall(pattern, text)
print(res)