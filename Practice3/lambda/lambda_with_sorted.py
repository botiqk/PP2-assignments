#1 example

students = [("Emil", 25), ("Tobias", 22), ("Linus", 28)]
sorted_students = sorted(students, key=lambda x: x[1])
print(sorted_students)

#2 example

words = ["apple", "pie", "banana", "cherry"]
sorted_words = sorted(words, key=lambda x: len(x))
print(sorted_words)

#3 example

numbers = [5, 2, 9, 1, 7]
result = sorted(numbers)
print(result)  

#4 example

numbers = [5, 2, 9, 1, 7]
result = sorted(numbers, key=lambda x: -x)
print(result) 