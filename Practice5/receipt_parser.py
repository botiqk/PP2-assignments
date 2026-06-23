import re
import json

#read a file
with open("raw.txt", "r", encoding="utf-8") as f:
    text = f.read()

#extracting all prices
prices = re.findall(r"\d+\s?\d*,\d{2}", text)

#remove spaces in numbers
prices = [p.replace(" ", "") for p in prices]

#extracting names of products
products = re.findall(r"\d+\.\n(.+)", text)

#extracting dates and time
datetime_match = re.search(r"\d{2}\.\d{2}\.\d{4}\s\d{2}:\d{2}:\d{2}", text)

date = None
time = None

if datetime_match:
    dt = datetime_match.group()
    date, time = dt.split()

#determine payment method
payment = re.search(r"Банковская карта|Наличные|Карта", text)

payment_method = payment.group() if payment else None

#get overall sum from ticket
total_match = re.search(r"ИТОГО:\n([\d\s,]+)", text)

total = None
if total_match:
    total = total_match.group(1).replace(" ", "")

#determine general sum(by products price)
total_calc = sum(float(p.replace(",", ".")) for p in prices)

#form data structures(json)
data = {
    "products": products,
    "prices": prices,
    "total": total_calc,
    "date": date,
    "time": time,
    "payment_method": payment_method
}

#res (python -> json)
print(json.dumps(data, indent=4, ensure_ascii=False))