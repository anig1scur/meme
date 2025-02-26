import json
import csv
import os

BASE = os.path.join(os.path.dirname(__file__), "../public")
details_file = os.path.join(BASE, "meme_details.json")
stats_file = os.path.join(BASE, "meme_stats.json")

with open(details_file, "r", encoding="utf-8") as f:
    memes_data = json.load(f)

for meme in memes_data:
    meme_id = meme["image"].split(".")[0].lower()
    csv_file = os.path.join(BASE, "top/trending", f"{meme_id}.csv")
    google_trend_data = []

    if os.path.exists(csv_file):
        with open(csv_file, "r", encoding="utf-8") as csv_f:
            reader = csv.reader(csv_f)
            next(reader)
            next(reader)
            next(reader)
            for row in reader:
                if len(row) > 1:
                    t = 0
                    try:
                        t = int(row[1])
                    except Exception:
                        pass
                    google_trend_data.append(t)
    if not google_trend_data:
        google_trend_data = None

    meme["trend"] = google_trend_data
    meme.pop("about", None)
    meme.pop("origin_story", None)
    meme.pop("imgflip", None)

with open(stats_file, "w", encoding="utf-8") as f:
    json.dump(memes_data, f, ensure_ascii=False, indent=None, separators=(',', ':'))
