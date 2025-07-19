import feedparser
import json
from datetime import datetime

note_rss = "https://note.com/y_tantan1359/rss"
booklog_rss = "https://booklog.jp/users/tantan1359/feed"

def parse_rss(feed_url, platform_name):
    feed = feedparser.parse(feed_url)
    logs = []
    for entry in feed.entries[:5]:
        if hasattr(entry, "published_parsed") and entry.published_parsed:
            date_struct = entry.published_parsed
        elif hasattr(entry, "updated_parsed") and entry.updated_parsed:
            date_struct = entry.updated_parsed
        else:
            date_struct = datetime.utcnow().timetuple()

        logs.append({
            "date": datetime(*date_struct[:6]).strftime("%Y-%m-%d"),
            "title": entry.title,
            "link": entry.link,
            "platform": platform_name
        })
    return logs

note_logs = parse_rss(note_rss, "note")
booklog_logs = parse_rss(booklog_rss, "ブクログ")

all_logs = note_logs + booklog_logs
all_logs.sort(key=lambda x: x["date"], reverse=True)

with open('logs.json', 'w', encoding='utf-8') as f:
    json.dump(all_logs, f, ensure_ascii=False, indent=4)
