from urllib.parse import urlparse, urlunparse


TRACKING_PARAMETERS = {
    "utm_source",
    "utm_medium",
    "utm_campaign",
    "utm_term",
    "utm_content",
    "at_medium",
    "at_campaign",
}

def normalize_url(url: str) -> str:
    parsed = urlparse(url)

    query_parts = []

    if parsed.query:
        for parameter in parsed.query.split("&"):
            if "=" in parameter:
                key, value = parameter.split("=", 1)

                if key not in TRACKING_PARAMETERS:
                    query_parts.append(f"{key}={value}")
            else:
                if parameter not in TRACKING_PARAMETERS:
                    query_parts.append(parameter)

    normalized_query = "&".join(query_parts)

    return urlunparse(
        (
            parsed.scheme.lower(),
            parsed.netloc.lower(),
            parsed.path.rstrip("/"),
            parsed.params,
            normalized_query,
            "",
        )
    )
    
def detect_content_type(url: str) -> str:
    if "/news/videos/" in url:
        return "video"

    return "article"