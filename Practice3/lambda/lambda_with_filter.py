#1 example

numbers = [1, 2, 3, 4, 5, 6, 7, 8]
odd_numbers = list(filter(lambda x: x % 2 != 0, numbers))
print(odd_numbers)

#2 example

nums = [1,2,3,4,5,6,7,8,9]
evens = list(filter(lambda a : a % 2 == 0, nums))
print(*evens)

#3 example

words = ["cat", "apple", "hi", "banana"]
long_words = list(filter(lambda x: len(x) > 3, words))
print(long_words)  

#4 example

numbers = [-5, 3, 0, -2, 8]
posnum = list(filter(lambda x: x > 0, numbers))
print(posnum) 