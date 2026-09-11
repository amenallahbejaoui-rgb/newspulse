from bs4 import BeautifulSoup

from .url import detect_content_type


def parse_article(html: str, url: str) -> dict:
    soup = BeautifulSoup(html, "html.parser")

    content_type = detect_content_type(url)

    title = ""

    if soup.title:
        title = soup.title.get_text(strip=True)

        if " - BBC News" in title:
            title = title.replace(" - BBC News", "")

    description = ""

    meta_description = soup.find(
        "meta",
        attrs={"name": "description"},
    )

    if meta_description:
        description = meta_description.get("content", "").strip()

    paragraphs = []

    if content_type == "article":
        for paragraph in soup.find_all("p"):
            text = paragraph.get_text(" ", strip=True)

            if text and text != title:
                paragraphs.append(text)

    return {
        "title": title,
        "description": description,
        "content": "\n\n".join(paragraphs),
        "content_type": content_type,
    }