from scraper.article import fetch_article_page
from parser.article import parse_article


url = "https://www.bbc.co.uk/news/videos/c74knp7y04eo"
html = fetch_article_page(url)

article = parse_article(html, url)

print("TITLE:")
print(article["title"])

print("\nDESCRIPTION:")
print(article["description"])

print("\nCONTENT:")
print(article["content"][:3000])
print("\nCONTENT TYPE:")
print(article["content_type"])