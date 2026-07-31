import re, csv, json, sqlite3, statistics, requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import pandas as pd

#TASK-1 : starting scraping
BASE="https://books.toscrape.com/"
RATE=105.50
CATS={
    "Travel":"catalogue/category/books/travel_2/index.html",
    "Mystery":"catalogue/category/books/mystery_3/index.html",
    "Classics":"catalogue/category/books/classics_6/index.html"
}
MAP={"One":1,"Two":2,"Three":3,"Four":4,"Five":5}

def price(x):
    m=re.search(r"\d+\.?\d*",x)
    return float(m.group()) if m else None

raw=[]; prices=[]; ratings=[]

for cat,path in CATS.items():
    url=urljoin(BASE,path)
    while url:
        s=BeautifulSoup(requests.get(url,timeout=10).text,"html.parser")
        for p in s.select("article.product_pod"):
            pr=price(p.select_one(".price_color").text)
            rt=next((c for c in p.select_one(".star-rating")["class"] if c in MAP),None)
            raw.append({
                "title":p.h3.a["title"],
                "price":pr,
                "rating":MAP.get(rt,3),
                "stock":"in stock" in p.select_one(".availability").text.lower(),
                "category":cat
            })
            if pr: prices.append(pr)
            ratings.append(MAP.get(rt,3))
        nxt=s.select_one("li.next a")
        url=urljoin(url,nxt["href"]) if nxt else None

#TASK-2 & 3 : cleaning data & converting price_gbp to a price_inr
pm=statistics.median(prices); rm=round(statistics.median(ratings))
rows=[{
"title":r["title"],
"price_gbp":r["price"] or pm,
"price_inr":round((r["price"] or pm)*RATE,2),
"rating":r["rating"] or rm,
"in_stock":int(r["stock"]),
"category":r["category"]
} for r in raw]

with open("books_dataset.csv","w",newline="",encoding="utf-8") as f:
    w=csv.DictWriter(f,fieldnames=rows[0].keys()); w.writeheader(); w.writerows(rows)

print("Total scraped rows:", len(raw))
print("Rows dropped:", 0)   
print("Using price median:", pm)
print("Using rating median:", rm)
print("Clean rows saved:", len(rows))
print("Saved cleaned book data to books_dataset.csv")

#TASK-4 : sqlite schema creation

print("\nStarting Database...")
conn = sqlite3.connect("books.db")
cur = conn.cursor()
cur.executescript("""
DROP TABLE IF EXISTS books;
DROP TABLE IF EXISTS categories;

CREATE TABLE categories(
    category_id INTEGER PRIMARY KEY AUTOINCREMENT,
    category_name TEXT UNIQUE
);

CREATE TABLE books(
    book_id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT,
    price_gbp REAL,
    price_inr REAL,
    rating INTEGER,
    in_stock INTEGER,
    category_id INTEGER,
    FOREIGN KEY(category_id) REFERENCES categories(category_id)
);
""")
print("Tables Created")
ids = {}
for c in sorted({r["category"] for r in rows}):
    cur.execute(
        "INSERT INTO categories(category_name) VALUES(?)",
        (c,)
    )
    ids[c] = cur.lastrowid

print("Categories Inserted:", len(ids))

cur.executemany("""
INSERT INTO books
(title,price_gbp,price_inr,rating,in_stock,category_id)
VALUES(?,?,?,?,?,?)
""", [
    (
        r["title"],
        r["price_gbp"],
        r["price_inr"],
        r["rating"],
        r["in_stock"],
        ids[r["category"]]
    )
    for r in rows
])
conn.commit()
print("Books Inserted:", len(rows))

cur.execute("""
SELECT
    b.title,
    b.price_gbp,
    b.price_inr,
    b.rating,
    b.in_stock,
    c.category_name
FROM books b
JOIN categories c
ON b.category_id = c.category_id
ORDER BY c.category_name, b.title
LIMIT 5;
""")

print("\nSample Joined Rows:")
for row in cur.fetchall():
    print(row)

#TASK-5 : queries execution and storing results in json
queries={
"Q1":"SELECT title,price_gbp,rating FROM books WHERE in_stock=1;",
"Q2":"SELECT title,price_gbp FROM books ORDER BY price_gbp DESC LIMIT 5;",
"Q3":"SELECT DISTINCT rating FROM books ORDER BY rating;",
"Q4":"SELECT title,price_gbp FROM books WHERE price_gbp BETWEEN 10 AND 20;",
"Q5":"SELECT title,rating FROM books WHERE rating IN (4,5);",
"Q6":"SELECT c.category_name,b.title,b.rating FROM books b JOIN categories c ON b.category_id=c.category_id LIMIT 5;"
}
results = {}
for name, q in queries.items():
    cur.execute(q)
    cols = [d[0] for d in cur.description]
    data = cur.fetchall()
    results[name] = {
        "sql": q,
        "columns": cols,
        "rows": data
    }
    print("=" * 20)
    print(name)
    print(q.strip())
    print("-" * 20)
    print(cols)

    for r in data:
        print(r)
    print(f"({len(data)} rows)\n")

with open("query_results.json", "w", encoding="utf-8") as f:
    json.dump(results, f, indent=2, default=str)

print("Saved all query strings and outputs to query_results.json")

#TASK-6 : Read two query results into DataFrames
#TASK-6
q1 = pd.read_sql(queries["Q1"], conn)
q2 = pd.read_sql(queries["Q2"], conn)

print(q1)
print(q2)

books = pd.read_sql("SELECT * FROM books;", conn)
cats = pd.read_sql("SELECT * FROM categories;", conn)

merge_df = pd.merge(books, cats, on="category_id")[[
    "title","price_gbp","price_inr","rating","in_stock","category_name"
]].sort_values(["category_name","title"]).head(5).reset_index(drop=True)

sql_df = pd.read_sql("""
SELECT b.title,b.price_gbp,b.price_inr,b.rating,b.in_stock,c.category_name
FROM books b
JOIN categories c
ON b.category_id=c.category_id
ORDER BY c.category_name,b.title
LIMIT 5;
""", conn)

print("\nSQL JOIN and pd.merge() produce the same output:",merge_df.equals(sql_df))
conn.close()
print("Database connection closed.")