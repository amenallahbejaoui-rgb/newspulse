from scraper.article import fetch_article_page


url = "https://www.bbc.co.uk/news/videos/c74knp7y04eo"

html = fetch_article_page(url)

print("HTML LENGTH:", len(html))
print("FIRST 500 CHARACTERS:")
print(html[:500])