#1 example

import datetime

x = datetime.datetime.now()
print(x)

#2 example

import datetime

x = datetime.datetime(2020, 5, 17)

print(x)

#3 example

import datetime

x = datetime.datetime(2018, 6, 1)

print(x.strftime("%B"))

#4 example

import datetime

obj = datetime.datetime(2001, 11, 15, 1, 20, 25)

# checking timezone information
print(obj.tzinfo)