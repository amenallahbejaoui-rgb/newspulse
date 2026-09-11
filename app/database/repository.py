from datetime import datetime

from sqlalchemy import select
from sqlalchemy.orm import Session

from .models import Article


def article_exists(session: Session, url: str) -> bool:
    statement = select(Article).where(Article.url == url)

    return session.execute(statement).scalar_one_or_none() is not None


def save_article(
    session: Session,
    article_data: dict,
) -> Article | None:

    url = article_data.get("url", "").strip()

    if not url:
        return None

    if article_exists(session, url):
        return None

    article = Article(
        title=article_data["title"],
        url=url,
        summary=article_data.get("summary"),
        content=article_data.get("content"),
        published=article_data.get("published"),
        source=article_data["source"],
        category=article_data["category"],
        content_type=article_data.get(
            "content_type",
            "article",
        ),
        scraped_at=article_data.get("scraped_at"),
    )

    session.add(article)

    return article


def save_articles(
    session: Session,
    articles: list[dict],
) -> list[Article]:

    new_articles = []

    for article_data in articles:
        article = save_article(
            session,
            article_data,
        )

        if article is not None:
            new_articles.append(article)

    session.commit()

    return new_articles


def update_article_content(
    session: Session,
    article: Article,
    content: str | None,
    content_type: str,
):
    article.content = content
    article.content_type = content_type
    article.scraped_at = datetime.now()

    session.commit()