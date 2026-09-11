from datetime import datetime
import sys
from pathlib import Path


if __package__ is None:
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from app.database.database import SessionLocal
from app.database.models import Article
from app.scraper.article import fetch_article_page
from app.parser.article import parse_article
from app.parser.url import detect_content_type


with SessionLocal() as session:

    articles = session.query(Article).all()

    print(f"Articles to process: {len(articles)}")

    for index, article in enumerate(articles, start=1):

        print()
        print(f"[{index}/{len(articles)}] {article.title}")

        content_type = detect_content_type(article.url)

        print(f"Type: {content_type}")

        if content_type == "video":
            article.content_type = "video"
            article.content = None
            article.scraped_at = datetime.utcnow()

            print("Skipped video")

            continue

        try:
            html = fetch_article_page(article.url)

            parsed = parse_article(
                html,
                article.url,
            )

            article.content = parsed["content"]
            article.content_type = parsed["content_type"]
            article.scraped_at = datetime.utcnow()

            print(
                f"Scraped: "
                f"{len(article.content)} characters"
            )

        except Exception as error:
            print(f"ERROR: {error}")

    session.commit()

    print()
    print("================================")
    print("SCRAPING COMPLETE")
    print("================================")