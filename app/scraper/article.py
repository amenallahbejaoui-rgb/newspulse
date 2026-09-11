import httpx


def fetch_article_page(url: str) -> str:
    headers = {
        "User-Agent": (
            "Mozilla/5.0 "
            "(Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 "
            "(KHTML, like Gecko) "
            "Chrome/140.0.0.0 Safari/537.36"
        )
    }

    response = httpx.get(
        url,
        headers=headers,
        timeout=10.0,
        follow_redirects=True,
    )

    response.raise_for_status()

    return response.text