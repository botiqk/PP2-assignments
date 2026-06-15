#1 example
x = 5
y = "John"
print(x)
print(y)

x = str(3)    # x will be '3'
y = int(3)    # y will be 3
z = float(3)  # z will be 3. 0

x = 5
y = "John"
print(type(x))
print(type(y))

#2 var names
myvar = "John"
my_var = "John"
_my_var = "John"
myVar = "John"
MYVAR = "John"
myvar2 = "John"

#3 multiple 
x, y, z = "Orange", "Banana", "Cherry"
print(x)
print(y)
print(z)

#4 output var
x = "Python"
y = "is"
z = "awesome"
print(x, y, z)

#5 glob var
x = "awesome"

def myfunc():
  x = "fantastic"
  print("Python is " + x)

myfunc()

print("Python is " + x)