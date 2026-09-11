from .url import normalize_url


def deduplicate_articles(articles: list[dict]) -> list[dict]:
    seen_urls = set()
    unique_articles = []

    for article in articles:
        url = article.get("url", "").strip()

        if not url:
            continue

        normalized_url = normalize_url(url)

        if normalized_url in seen_urls:
            continue

        seen_urls.add(normalized_url)

        article["url"] = normalized_url

        unique_articles.append(article)

    return unique_articles