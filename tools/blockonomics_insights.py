from email.utils import parsedate_to_datetime
import feedparser
import requests


def fetch_blockonomics_rss_compact(max_items: int = 25) -> list[dict]:
    """
    This tool retrieves Blockonomics the latest rss compact feed
    :rtype: list[dict]
    """
    r = requests.get("https://insights.blockonomics.co/rss/", timeout=20)
    r.raise_for_status()
    feed = feedparser.parse(r.text)

    items = []
    for e in feed.entries[:max_items]:
        dt = None
        if getattr(e, "published", None):
            try: dt = parsedate_to_datetime(e.published)
            except Exception: pass
        items.append({
            "title": getattr(e, "title", None),
            "url": getattr(e, "link", None),
            "date": (dt.date().isoformat() if dt else None),
        })
    return items