from parser.url import detect_content_type


urls = [
    "https://www.bbc.co.uk/news/videos/c74knp7y04eo",
    "https://www.bbc.co.uk/news/articles/cly4x4e7q4eo",
]


for url in urls:
    print()
    print("URL:", url)
    print("TYPE:", detect_content_type(url))