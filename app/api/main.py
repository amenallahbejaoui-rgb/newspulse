from fastapi import FastAPI, Query
from ..database.database import SessionLocal
from ..database.queries import get_latest_articles
from fastapi.middleware.cors import CORSMiddleware
from ..database.models import Article
from contextlib import asynccontextmanager

from app.scheduler.jobs import start_scheduler, stop_scheduler

from sqlalchemy import select, func



@asynccontextmanager
async def lifespan(app: FastAPI):
    start_scheduler()
    yield
    stop_scheduler()


app = FastAPI(
    title="NewsPulse API",
    version="1.0.0",
    lifespan=lifespan,
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@asynccontextmanager
async def lifespan(app: FastAPI):
    start_scheduler()

    yield

    stop_scheduler()
@app.get("/health")
def health():
    return {
        "status": "ok",
        "service": "NewsPulse API",
    }


@app.get("/articles")
def get_articles(
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    category: str | None = None,
    source: str | None = None,
    search: str | None = None,
):

    with SessionLocal() as session:

        statement = select(Article)

        if category:
            statement = statement.where(
                Article.category == category
            )

        if source:
            statement = statement.where(
                Article.source == source
            )

        if search:
            statement = statement.where(
                Article.title.ilike(f"%{search}%")
            )

        count_statement = select(
            func.count()
        ).select_from(statement.subquery())

        total = session.execute(
            count_statement
        ).scalar_one()

        statement = (
            statement
            .order_by(Article.id.desc())
            .offset((page - 1) * limit)
            .limit(limit)
        )

        articles = session.execute(
            statement
        ).scalars().all()

        return {
            "page": page,
            "limit": limit,
            "total": total,
            "pages": (total + limit - 1) // limit,
            "articles": [
                {
                    "id": article.id,
                    "title": article.title,
                    "url": article.url,
                    "summary": article.summary,
                    "content": article.content,
                    "published": article.published,
                    "source": article.source,
                    "category": article.category,
                    "content_type": article.content_type,
                    "created_at": article.created_at,
                    "scraped_at": article.scraped_at,
                }
                for article in articles
            ],
        }


@app.get("/articles/{article_id}")
def get_article(article_id: int):

    with SessionLocal() as session:

        article = session.get(
            Article,
            article_id,
        )

        if not article:
            return {
                "error": "Article not found"
            }

        return {
            "id": article.id,
            "title": article.title,
            "url": article.url,
            "summary": article.summary,
            "content": article.content,
            "published": article.published,
            "source": article.source,
            "category": article.category,
            "content_type": article.content_type,
            "created_at": article.created_at,
            "scraped_at": article.scraped_at,
        }


@app.get("/categories")
def get_categories():

    with SessionLocal() as session:

        statement = (
            select(Article.category)
            .distinct()
            .order_by(Article.category)
        )

        categories = session.execute(
            statement
        ).scalars().all()

        return {
            "categories": categories
        }


@app.get("/sources")
def get_sources():

    with SessionLocal() as session:

        statement = (
            select(Article.source)
            .distinct()
            .order_by(Article.source)
        )

        sources = session.execute(
            statement
        ).scalars().all()

        return {
            "sources": sources
        }


@app.get("/stats")
def get_stats():

    with SessionLocal() as session:

        total = session.execute(
            select(func.count()).select_from(Article)
        ).scalar_one()

        articles = session.execute(
            select(func.count())
            .select_from(Article)
            .where(Article.content_type == "article")
        ).scalar_one()

        videos = session.execute(
            select(func.count())
            .select_from(Article)
            .where(Article.content_type == "video")
        ).scalar_one()

        categories = session.execute(
            select(func.count(func.distinct(Article.category)))
        ).scalar_one()

        return {
            "total": total,
            "articles": articles,
            "videos": videos,
            "categories": categories,
        }