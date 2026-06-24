#Create nested folders

import os

os.makedirs("Practice6/folder1/folder2", exist_ok=True)

print("Directories created.")

#Show all files and folders in current directory

import os

print(os.listdir())

#find all files with ".txt"

import os

for file in os.listdir():
    if file.endswith(".txt"):
        print(file)

#curr directory

print(os.getcwd())