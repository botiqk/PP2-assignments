from datetime import date, timedelta

today = date.today()
subs = date.today() - timedelta(days = 5)

print("Today: " , today)
print("Substraction: " , subs)