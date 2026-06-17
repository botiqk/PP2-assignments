#1 example

mytuple = ("apple", "banana", "cherry")
myit = iter(mytuple)

print(next(myit))
print(next(myit))
print(next(myit))

#2 example

mytuple = ("apple", "banana", "cherry")

for x in mytuple:
  print(x) 

#3 example

class MyNumbers:
  def __iter__(self):
    self.a = 1
    return self

  def __next__(self):
    x = self.a
    self.a += 1
    return x

myclass = MyNumbers()
myiter = iter(myclass)

print(next(myiter))
print(next(myiter))
print(next(myiter))
print(next(myiter))
print(next(myiter)) #output : 1 -> 20

#4 example

def fun(max):
    cnt = 1
    while cnt <= max:
        yield cnt
        cnt += 1

ctr = fun(5)
for n in ctr:
    print(n) #output : 1,2,3,4,5

#5 example

def fun():
    yield 1            
    yield 2            
    yield 3            
 
# Driver code to check above generator function
for val in fun(): 
    print(val) #output : 1,2,3

#6 example

sq = (x*x for x in range(1, 6))
for i in sq:
    print(i) #output : 4,9,16,25