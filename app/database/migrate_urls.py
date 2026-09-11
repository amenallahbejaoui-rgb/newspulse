import sys
from pathlib import Path


if __package__ is None:
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from app.database.database import SessionLocal
from app.database.models import Article
from app.parser.url import normalize_url


with SessionLocal() as session:

    articles = session.query(Article).all()

    updated = 0

    for article in articles:
        normalized_url = normalize_url(article.url)

        if normalized_url != article.url:
            article.url = normalized_url
            updated += 1

    session.commit()

    print(f"URLs checked: {len(articles)}")
    print(f"URLs normalized: {updated}")