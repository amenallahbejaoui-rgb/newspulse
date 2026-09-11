# NewsPulse

NewsPulse is an automated news aggregation and processing platform that collects articles from multiple sources, extracts their content, removes duplicates, classifies content types, and organizes the resulting data through a web dashboard.

### Stack

Python · FastAPI · SQLAlchemy · SQLite · BeautifulSoup · feedparser · APScheduler · Next.js · TypeScript · Tailwind CSS

### Pipeline

```text
RSS Sources
    ↓
RSS Ingestion
    ↓
URL Normalization
    ↓
Deduplication
    ↓
Article Extraction
    ↓
Database
    ↓
FastAPI
    ↓
Next.js Dashboard
```

### Built

* Multi-source RSS ingestion
* Article extraction
* URL normalization and deduplication
* Article/video classification
* Search and filtering
* Scheduled processing
* REST API
* Web dashboard

