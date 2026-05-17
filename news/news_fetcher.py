"""
News fetcher for government schemes and commodity price updates.
Uses Google News RSS — no API key required.
"""
import ssl
import feedparser
from datetime import datetime, timezone
from typing import List, Dict
from loguru import logger

# Patch SSL for environments with certificate issues
ssl._create_default_https_context = ssl._create_unverified_context

FEEDS = [
    {
        "category": "🏛️ Government Schemes",
        "queries": [
            "government scheme rice wheat edible oil India",
            "PM Garib Kalyan Anna Yojana PMGKAY India",
            "FCI food corporation India rice procurement",
            "NFSA PDS ration card food security India",
        ],
    },
    {
        "category": "🌾 Rice Market",
        "queries": [
            "rice price India market 2026",
            "basmati non-basmati rice export India",
            "rice MSP minimum support price India",
        ],
    },
    {
        "category": "🫙 Edible Oil Market",
        "queries": [
            "edible oil price India mustard soybean sunflower",
            "palm oil import India price",
            "edible oil government policy India 2026",
        ],
    },
    {
        "category": "📊 Commodity & Trade Policy",
        "queries": [
            "food commodity price India wholesale market",
            "import export duty rice edible oil India",
            "inflation food prices India",
        ],
    },
]

BASE_URL = "https://news.google.com/rss/search?q={query}&hl=en-IN&gl=IN&ceid=IN:en"


def _parse_date(entry) -> datetime:
    try:
        t = entry.get("published_parsed")
        if t:
            return datetime(*t[:6], tzinfo=timezone.utc)
    except Exception:
        pass
    return datetime.now(timezone.utc)


def fetch_category(category_cfg: Dict, max_per_query: int = 5) -> List[Dict]:
    """Fetch and deduplicate news for one category."""
    seen_titles = set()
    articles = []

    for query in category_cfg["queries"]:
        url = BASE_URL.format(query=query.replace(" ", "+"))
        try:
            feed = feedparser.parse(url)
            for entry in feed.entries[:max_per_query]:
                title = entry.get("title", "").strip()
                if not title or title in seen_titles:
                    continue
                seen_titles.add(title)
                # Clean source from title  "Headline - Source Name" → separate
                source = ""
                if " - " in title:
                    parts = title.rsplit(" - ", 1)
                    title = parts[0].strip()
                    source = parts[1].strip()

                articles.append({
                    "title": title,
                    "source": source,
                    "link": entry.get("link", ""),
                    "published": _parse_date(entry),
                    "summary": entry.get("summary", "")[:300],
                })
        except Exception as e:
            logger.warning(f"Failed to fetch '{query}': {e}")

    # Sort newest first
    articles.sort(key=lambda x: x["published"], reverse=True)
    return articles[:5]


def fetch_all_news() -> Dict[str, List[Dict]]:
    """Fetch all categories. Returns {category_label: [articles]}."""
    result = {}
    for cfg in FEEDS:
        logger.info(f"Fetching news: {cfg['category']}")
        result[cfg["category"]] = fetch_category(cfg)
    return result
