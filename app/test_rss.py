from scraper.rss import fetch_rss
from scraper.sources import RSS_SOURCES
from parser.deduplicator import deduplicate_articles

from database.database import SessionLocal
from database.repository import save_articles


all_articles = []

for source in RSS_SOURCES:
    print(f"\n=== {source['name']} ===")

    articles = fetch_rss(source["url"])

    for article in articles:
        article["source"] = source["name"]
        article["category"] = source["category"]

    all_articles.extend(articles)

    print(f"Found {len(articles)} articles")


print("\n==============================")
print(f"RAW ARTICLES: {len(all_articles)}")
print("==============================")


unique_articles = deduplicate_articles(all_articles)


print("\n==============================")
print(f"UNIQUE ARTICLES: {len(unique_articles)}")
print(
    f"DUPLICATES REMOVED: "
    f"{len(all_articles) - len(unique_articles)}"
)
print("==============================")


with SessionLocal() as session:
    saved_count = save_articles(session, unique_articles)


print("\n==============================")
print(f"NEW ARTICLES SAVED: {saved_count}")
print("==============================")