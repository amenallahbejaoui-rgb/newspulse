from database.database import SessionLocal
from database.queries import get_latest_articles


with SessionLocal() as session:

    articles = get_latest_articles(session, limit=5)

    print(f"Found {len(articles)} articles")

    for article in articles:
        print()
        print("ID:", article.id)
        print("TITLE:", article.title)
        print("SOURCE:", article.source)
        print("CATEGORY:", article.category)
        print("URL:", article.url)