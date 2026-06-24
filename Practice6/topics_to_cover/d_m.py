#1 example : create a folder

import os

os.mkdir("my_folder")

#2 example : create subfolders

import os

os.makedirs("folder1/folder2/folder3")

#3 example : show the contents of the current folder

import os

print(os.listdir())

#4 example : move to another folder

import os

os.chdir("my_folder")
print(os.getcwd())

#5 example : show current directory

import os

print(os.getcwd())

#6 example : delete empty folder

import os

os.rmdir("my_folder")