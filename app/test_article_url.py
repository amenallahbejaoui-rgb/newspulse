from database.database import SessionLocal
from database.queries import get_latest_articles
from parser.url import detect_content_type


with SessionLocal() as session:

    articles = get_latest_articles(session, limit=20)

    for article in articles:
        content_type = detect_content_type(article.url)

        if content_type == "article":
            print("TITLE:", article.title)
            print("URL:", article.url)
            print("TYPE:", content_type)
            break