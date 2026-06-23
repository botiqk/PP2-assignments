import re
import json

with open("raw.txt", "r", encoding="utf-8") as file:
    text = file.read()

datetime_match = re.search(
    r"Время:\s*(\d{2}\.\d{2}\.\d{4})\s+(\d{2}:\d{2}:\d{2})",
    text
)

date = datetime_match.group(1) if datetime_match else None
time = datetime_match.group(2) if datetime_match else None

payment_match = re.search(r"(Банковская карта|Наличные):", text)
payment_method = payment_match.group(1) if payment_match else None

total_match = re.search(r"ИТОГО:\s*\n([\d\s]+,\d{2})", text)

total_amount = None
if total_match:
    total_amount = float(
        total_match.group(1)
        .replace(" ", "")
        .replace(",", ".")
    )

product_pattern = re.compile(
    r"\d+\.\s*\n(.*?)\n\d+,\d+\s*x\s*[\d\s]+,\d{2}\n([\d\s]+,\d{2})",
    re.MULTILINE
)

products = []
prices = []

for match in product_pattern.finditer(text):
    name = " ".join(match.group(1).split())

    price = float(
        match.group(2)
        .replace(" ", "")
        .replace(",", ".")
    )

    products.append(name)
    prices.append(price)

result = {
    "date": date,
    "time": time,
    "payment_method": payment_method,
    "total_amount": total_amount,
    "products": products,
    "prices": prices
}

print(json.dumps(result, ensure_ascii=False, indent=4))