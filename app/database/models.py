from datetime import datetime

from sqlalchemy import String, Text, DateTime
from sqlalchemy.orm import Mapped, mapped_column

from .database import Base


class Article(Base):
    __tablename__ = "articles"

    id: Mapped[int] = mapped_column(primary_key=True)

    title: Mapped[str] = mapped_column(String(500))

    url: Mapped[str] = mapped_column(
        String(1000),
        unique=True,
        index=True,
    )

    summary: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    content: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    published: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    source: Mapped[str] = mapped_column(
        String(100),
    )

    category: Mapped[str] = mapped_column(
        String(100),
    )

    content_type: Mapped[str] = mapped_column(
        String(50),
        default="article",
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
    )

    scraped_at: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True,
    )