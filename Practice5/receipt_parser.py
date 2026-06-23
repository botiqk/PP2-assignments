import re
import json

with open("raw.txt", "r", encoding="utf-8") as f:
    text = f.read()

dt = re.search(r"Время:\s*(\d{2}\.\d{2}\.\d{4})\s+(\d{2}:\d{2}:\d{2})", text)
date = dt.group(1) if dt else None
time = dt.group(2) if dt else None

payment = re.search(r"Банковская карта|Наличные", text)
payment_method = payment.group() if payment else None

products = re.findall(r"\d+\.\n(.+)", text)

prices = re.findall(r"Стоимость\n([\d\s]+,\d{2})", text)
prices = [float(p.replace(" ", "").replace(",", ".")) for p in prices]

total_amount = sum(prices)

result = {
    "date": date,
    "time": time,
    "payment_method": payment_method,
    "products": products,
    "prices": prices,
    "total_amount": total_amount
}

print(json.dumps(result, ensure_ascii=False, indent=4))