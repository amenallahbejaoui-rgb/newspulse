
from datetime import datetime

from .database.database import SessionLocal
from .database.models import Article
from .database.repository import (
    save_articles,
    update_article_content,
)

from .scraper.rss import fetch_rss
from .scraper.sources import RSS_SOURCES
from .scraper.article import fetch_article_page

from .parser.deduplicator import deduplicate_articles
from .parser.article import parse_article


def run_pipeline() -> dict:
    print("=" * 60)
    print("NewsPulse pipeline started")
    print("=" * 60)

    # ---------------------------------------------------------
    # Counters
    # ---------------------------------------------------------

    scraped_count = 0
    failed_count = 0

    # ---------------------------------------------------------
    # 1. Fetch RSS feeds
    # ---------------------------------------------------------

    all_articles = []

    for source in RSS_SOURCES:
        print(f"Fetching: {source['name']}")

        try:
            articles = fetch_rss(source["url"])

            for article in articles:
                article["source"] = source["name"]
                article["category"] = source["category"]

            all_articles.extend(articles)

            print(f"  Found: {len(articles)}")

        except Exception as error:
            print(f"  ERROR: {error}")

    print(f"\nRaw articles: {len(all_articles)}")

    # ---------------------------------------------------------
    # 2. Deduplicate
    # ---------------------------------------------------------

    unique_articles = deduplicate_articles(all_articles)

    print(f"Unique articles: {len(unique_articles)}")

    print(
        f"Duplicates removed: "
        f"{len(all_articles) - len(unique_articles)}"
    )

    # ---------------------------------------------------------
    # 3. Save new articles
    # ---------------------------------------------------------

    with SessionLocal() as session:
        new_articles = save_articles(
            session,
            unique_articles,
        )

    saved_count = len(new_articles)

    print(f"New articles saved: {saved_count}")

    # ---------------------------------------------------------
    # 4. Scrape content for NEW articles only
    # ---------------------------------------------------------

    if new_articles:

        with SessionLocal() as session:

            print(
                f"\nNew articles waiting for scraping: "
                f"{len(new_articles)}"
            )

            for article in new_articles:

                print(
                    f"Scraping [{article.id}] "
                    f"{article.title[:70]}"
                )

                try:
                    html = fetch_article_page(
                        article.url
                    )

                    parsed = parse_article(
                        html,
                        article.url,
                    )

                    db_article = session.get(
                        Article,
                        article.id,
                    )

                    if db_article is None:
                        failed_count += 1

                        print(
                            f"  ERROR: Article "
                            f"{article.id} not found"
                        )

                        continue

                    update_article_content(
                        session,
                        db_article,
                        parsed["content"],
                        parsed["content_type"],
                    )

                    scraped_count += 1

                except Exception as error:
                    failed_count += 1

                    print(
                        f"  ERROR: {error}"
                    )

    # ---------------------------------------------------------
    # 5. Summary
    # ---------------------------------------------------------

    result = {
        "timestamp": datetime.now().isoformat(),
        "raw_articles": len(all_articles),
        "unique_articles": len(unique_articles),
        "new_articles": saved_count,
        "scraped_articles": scraped_count,
        "failed_articles": failed_count,
    }

    print("\n" + "=" * 60)
    print("Pipeline complete")
    print("=" * 60)

    for key, value in result.items():
        print(f"{key}: {value}")

    return result


if __name__ == "__main__":
    run_pipeline()

