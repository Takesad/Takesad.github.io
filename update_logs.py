import feedparser
import json
from datetime import datetime

note_rss = "https://note.com/y_tantan1359/rss"
booklog_rss = "https://booklog.jp/users/tantan1359/feed"

def parse_rss(feed_url, platform_name):
    feed = feedparser.parse(feed_url)
    logs = []
    for entry in feed.entries[:5]:
        # まず published 文字列を優先的に使う
        if hasattr(entry, "published"):
            try:
                # published 例: 'Sat, 20 Jul 2025 12:34:56 +0000'
                dt = datetime(*entry.published_parsed[:6])
            except Exception:
                # 文字列をパースできなかった場合は現在時刻
                dt = datetime.utcnow()
        elif hasattr(entry, "published_parsed") and entry.published_parsed:
            dt = datetime(*entry.published_parsed[:6])
        elif hasattr(entry, "updated_parsed") and entry.updated_parsed:
            dt = datetime(*entry.updated_parsed[:6])
        else:
            dt = datetime.utcnow()

        logs.append({
            "date": dt.strftime("%Y-%m-%d %H:%M:%S"),
            "title": entry.title,
            "link": entry.link,
            "platform": platform_name
        })
    return logs

# note と ブクログを取得
note_logs = parse_rss(note_rss, "note")
booklog_logs = parse_rss(booklog_rss, "ブクログ")

# 結合して日時でソート
all_logs = note_logs + booklog_logs
all_logs.sort(key=lambda x: datetime.strptime(x["date"], "%Y-%m-%d %H:%M:%S"), reverse=True)

# JSON に書き出し
with open('logs.json', 'w', encoding='utf-8') as f:
    json.dump(all_logs, f, ensure_ascii=False, indent=4)
