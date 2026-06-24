#1 example : to print current directory
import os

print(os.getcwd())

#2 example : to copy file
import shutil

shutil.copy("example.txt", "backup.txt")

print("File copied")

#3 example : work with paths

from pathlib import Path

path = Path("example.txt")

print(path.exists())
print(path.name)
print(path.suffix)
#output : True ; example.txt ; .txt