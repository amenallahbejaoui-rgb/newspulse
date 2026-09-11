from parser.url import normalize_url


urls = [
    "https://example.com/article/123",
    "https://example.com/article/123?utm_source=rss",
    "https://example.com/article/123?utm_source=rss&utm_campaign=news",
    "https://example.com/article/123?category=technology",
    "https://www.bbc.co.uk/news/videos/c74knp7y04eo?at_medium=RSS&at_campaign=rss",
]


for url in urls:
    print()
    print("ORIGINAL:  ", url)
    print("NORMALIZED:", normalize_url(url))