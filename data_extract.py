import requests
from bs4 import BeautifulSoup
from schema_evolution import create_table, insert_articles, fetch_latest_articles
from datetime import datetime
import hashlib


# Scrape Skift data

def scrape_skift():
    url = "https://skift.com/news/"
    response = requests.get(url, timeout=10)
    soup = BeautifulSoup(response.text, "html.parser")

    articles = []
    for item in soup.select("article.c-tease"):
        title_tag = item.select_one("h3.c-tease__title a")
        author_tag = item.select_one("div.c-tease__byline a")
        time_tag = item.select_one("div.c-tease__byline time")

        if not title_tag:
            continue

        title = title_tag.text.strip()
        link = title_tag["href"]
        author = author_tag.text.strip() if author_tag else "Unknown"
        published_at = time_tag["datetime"] if time_tag and "datetime" in time_tag.attrs else datetime.utcnow().isoformat()

        articles.append({
            "article_id": hashlib.sha256(link.encode()).hexdigest(),
            "url": link,
            "title": title,
            "author": author,
            "published_at": published_at,
            "source": "Skift"
        })

    return articles

# Scrape phocuswire data
def scrape_phocuswire():
    url = "https://www.phocuswire.com/Latest-News"
    response = requests.get(url, timeout=10)
    soup = BeautifulSoup(response.text, "html.parser")

    articles = []
    for item in soup.select("div.item-view"):
        link_tag = item.select_one("a.title")
        author_tag = item.select_one("div.author span.name")
        date_text = item.select_one("div.author").text.split("|")[-1].strip() if item.select_one("div.author") else None

        if not link_tag:
            continue

        title = link_tag.text.strip()
        link = link_tag["href"]
        author = author_tag.text.strip() if author_tag else "Unknown"
        try:
            published_at = datetime.strptime(date_text, "%B %d, %Y").isoformat()
        except:
            published_at = datetime.utcnow().isoformat()

        articles.append({
            "article_id": hashlib.sha256(link.encode()).hexdigest(),
            "url": link,
            "title": title,
            "author": author,
            "published_at": published_at,
            "source": "PhocusWire"
        })

    return articles

# Main Execution
if __name__ == "__main__":
    create_table()
    all_articles = scrape_skift()+scrape_phocuswire()
    insert_articles(all_articles)
    latest = fetch_latest_articles()
    print("Top 5 Latest Articles:\n")
    for i, (article_id,title, url, author, published_at, source) in enumerate(latest):
        print(f"{i+1}. article_id:{article_id} \n  source: {source}\n  title: {title}\n  author: {author}\n  Published: {published_at}\n URL: {url}\n")