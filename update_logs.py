import feedparser
import json
from datetime import datetime

note_rss = "https://note.com/y_tantan1359/rss"
booklog_rss = "https://booklog.jp/users/tantan1359/feed"

def parse_rss(feed_url, platform_name):
    feed = feedparser.parse(feed_url)
    logs = []
    for entry in feed.entries[:5]:
        # published_parsed か updated_parsed を取得
        if hasattr(entry, "published_parsed") and entry.published_parsed:
            date_struct = entry.published_parsed
        elif hasattr(entry, "updated_parsed") and entry.updated_parsed:
            date_struct = entry.updated_parsed
        else:
            date_struct = datetime.utcnow().timetuple()

        # datetime オブジェクトに変換（年月日 時:分:秒 まで）
        dt = datetime(*date_struct[:6])

        logs.append({
            "date": dt.strftime("%Y-%m-%d %H:%M:%S"),  # ← 時間まで入れる
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
