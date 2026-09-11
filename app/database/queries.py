from sqlalchemy import select
from sqlalchemy.orm import Session

from .models import Article


def get_latest_articles(
    session: Session,
    limit: int = 10,
) -> list[Article]:

    statement = (
        select(Article)
        .order_by(Article.id.desc())
        .limit(limit)
    )

    return list(session.execute(statement).scalars().all())


def get_articles_by_category(
    session: Session,
    category: str,
) -> list[Article]:

    statement = (
        select(Article)
        .where(Article.category == category)
        .order_by(Article.id.desc())
    )

    return list(session.execute(statement).scalars().all())