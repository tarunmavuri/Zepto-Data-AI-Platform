import re, statistics, requests, csv
from bs4 import BeautifulSoup

GBP_TO_INR_RATE = 105.50

BASE = "https://books.toscrape.com/"

CATEGORIES = {
    "Travel": "catalogue/category/books/travel_2/index.html",
    "Mystery": "catalogue/category/books/mystery_3/index.html",
    "Classics": "catalogue/category/books/classics_6/index.html",
}

RATING_MAP = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}

def parse_price(price):
    m = re.search(r"\d+\.?\d*", price.replace(",", ""))
    return float(m.group()) if m else None

def parse_rating(rating):
    return RATING_MAP.get(rating)

def parse_stock(stock):
    stock = stock.lower().strip()
    if "in stock" in stock:
        return True
    if "out of stock" in stock or "unavailable" in stock:
        return False
    return None

raw_rows, parsed_rows, price_values, rating_values, parse_errors = [], [], [], [], []

# Scrape data
for category, path in CATEGORIES.items():
    url = BASE + path
    while url:
        soup = BeautifulSoup(requests.get(url).text, "html.parser")

        for pod in soup.select("article.product_pod"):
            row = {
                "title": pod.h3.a["title"].strip(),
                "price": pod.select_one(".price_color").get_text(strip=True),
                "star_rating": next(
                    (c for c in pod.select_one(".star-rating")["class"] if c in RATING_MAP),
                    None,
                ),
                "availability": pod.select_one(".availability").get_text(strip=True),
                "category": category,
            }
            raw_rows.append(row)

        next_btn = soup.select_one("li.next a")
        url = url.rsplit("/", 1)[0] + "/" + next_btn["href"] if next_btn else None

# Parse data
for row in raw_rows:
    price = parse_price(row["price"])
    rating = parse_rating(row["star_rating"])
    stock = parse_stock(row["availability"])

    if price is not None:
        price_values.append(price)
    if rating is not None:
        rating_values.append(rating)

    parsed_rows.append({
        "raw": row,
        "price": price,
        "rating": rating,
        "stock": stock
    })

DEFAULT_PRICE = 0.0
DEFAULT_RATING = 3

price_median = statistics.median(price_values) if price_values else DEFAULT_PRICE
rating_median = round(statistics.median(rating_values)) if rating_values else DEFAULT_RATING

cleaned_rows = []

# Clean data and convert GBP to INR
for item in parsed_rows:
    row = item["raw"]
    price = item["price"] if item["price"] is not None else price_median
    rating = item["rating"] if item["rating"] is not None else rating_median

    if item["stock"] is None:
        parse_errors.append({
            "title": row["title"],
            "raw_availability": row["availability"]
        })
        continue

    cleaned_rows.append({
        "title": row["title"],
        "price_gbp": price,
        "price_inr": round(price * GBP_TO_INR_RATE, 2),
        "rating": rating,
        "in_stock": item["stock"],
        "category": row["category"],
    })

# Display summary
print("Total scraped rows:", len(raw_rows))
print("Rows dropped:", len(parse_errors))
print("Using price median:", price_median)
print("Using rating median:", rating_median)
print("Clean rows saved:", len(cleaned_rows))

# Save to CSV
with open("books_dataset.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(
        f,
        fieldnames=[
            "title",
            "price_gbp",
            "price_inr",
            "rating",
            "in_stock",
            "category",
        ],
    )
    writer.writeheader()
    writer.writerows(cleaned_rows)

print("Saved cleaned book data to books_dataset.csv")