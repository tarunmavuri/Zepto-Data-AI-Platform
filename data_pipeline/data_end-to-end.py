
import requests
from bs4 import BeautifulSoup
import csv
 
BASE = "https://books.toscrape.com/"
 
# 3 categories
CATEGORIES = {
    "Travel": "catalogue/category/books/travel_2/index.html",
    "Mystery": "catalogue/category/books/mystery_3/index.html",
    "Classics": "catalogue/category/books/classics_6/index.html",
}
 
STAR_WORDS = {"One", "Two", "Three", "Four", "Five"}
 
books = []
 
for category, path in CATEGORIES.items():
    url = BASE + path
    while url:
        res = requests.get(url)
        res.encoding = "utf-8"  
        soup = BeautifulSoup(res.text, "html.parser")
 
        for pod in soup.select("article.product_pod"):
            title = pod.h3.a["title"].strip()          # full title
            price = pod.select_one(".price_color").get_text(strip=True)
            availability = pod.select_one(".availability").get_text(strip=True)
            rating_class = pod.select_one(".star-rating")["class"]
            star_rating = next(c for c in rating_class if c in STAR_WORDS)
 
            books.append({
                "title": title,
                "price": price,
                "star_rating": star_rating,
                "availability": availability,
                "category": category,
            })
 
        next_btn = soup.select_one("li.next a")
        url = url.rsplit("/", 1)[0] + "/" + next_btn["href"] if next_btn else None
 
# basic validation
print("Total books:", len(books))
missing = [b for b in books if not b["title"] or not b["price"]]
print("Rows with missing data:", len(missing))
 
# save
with open("books_dataset.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["title", "price", "star_rating", "availability", "category"])
    writer.writeheader()
    writer.writerows(books)
 
print("Saved to books_dataset.csv")
 
