import feedparser


def fetch_rss(url: str) -> list[dict]:
    feed = feedparser.parse(url)

    articles = []

    for entry in feed.entries:
        article = {
            "title": entry.get("title", "").strip(),
            "url": entry.get("link", "").strip(),
            "summary": entry.get("summary", "").strip(),
            "published": entry.get("published", "").strip(),
        }

        articles.append(article)

    return articles