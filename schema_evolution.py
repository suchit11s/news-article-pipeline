import sqlite3

DB_PATH = "news_articles.db"


# Create schema

def create_table():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
                   CREATE TABLE IF NOT EXISTS articles
                   (
                       article_id
                       TEXT
                       PRIMARY
                       KEY,
                       url
                       TEXT
                       NOT
                       NULL,
                       title
                       TEXT
                       NOT
                       NULL,
                       author
                       TEXT,
                       published_at
                       TEXT,
                       source
                       TEXT
                   )
                   """)
    conn.commit()
    conn.close()


# Insert new articles only
def insert_articles(articles):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    for article in articles:
        try:
            cursor.execute("""
                           INSERT INTO articles (article_id, url, title, author, published_at, source)
                           VALUES (?, ?, ?, ?, ?, ?)
                           """, (
                               article["article_id"],
                               article["url"],
                               article["title"],
                               article["author"],
                               article["published_at"],
                               article["source"]
                           ))
        except sqlite3.IntegrityError:
            # Skip duplicates based on article_id
            continue
    conn.commit()
    conn.close()


# Fetch top 5 latest articles
def fetch_latest_articles():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
                   SELECT article_id, title, url, author, published_at, source
                   FROM articles
                   ORDER BY datetime(published_at) DESC limit 5

                   """)
    rows = cursor.fetchall()
    conn.close()
    return rows