from datetime import date, timedelta

today = date.today()

yesterday = date.today() - timedelta(days = 1)
tomorrow = date.today() + timedelta(days = 1)

print("Yesterday: " , yesterday)
print("Today: " , today)
print("Tomorrow: " , tomorrow)