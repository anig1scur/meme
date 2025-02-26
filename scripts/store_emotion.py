import json
import re
import os

PUBLIC_BASE = os.path.join(os.path.dirname(__file__), "../public")
DATA_BASE = os.path.join(os.path.dirname(__file__), "../data")
json_file = os.path.join(PUBLIC_BASE, "meme_details.json")
md_file = os.path.join(DATA_BASE, "meme-sentiment-analysis.md")


def parse_markdown_table(md_file):
    with open(md_file, "r", encoding="utf-8") as f:
        lines = f.readlines()

    memes = {}
    for line in lines[4:]:
        if "|" in line and not line.startswith("|---------"):
            parts = [x.strip() for x in line.split("|")[1:-1]]
            if len(parts) == 5:
                meme_id = parts[0].replace(" ", "-")
                memes[meme_id] = [
                    int(parts[1]),
                    int(parts[2]),
                    int(parts[3]),
                    int(parts[4]),
                ]
    return memes


def extract_meme_name(imgflip_url):
    """
    - http://imgflip.com/meme/I-See-Dead-People
    - http://imgflip.com/meme/39633/Dinkleberg
    """
    match = re.search(r"meme/(?:\d+/)?([\w-]+)", imgflip_url)
    if match:
        return match.group(1).replace("_", "-")
    return None


def update_json_with_sentiment(json_file, md_data):
    with open(json_file, "r", encoding="utf-8") as f:
        json_data = json.load(f)

    for meme in json_data:
        meme_name = extract_meme_name(meme.get("imgflip", ""))
        if meme_name and meme_name in md_data:
            meme["emotion"] = md_data[meme_name]

    with open(json_file, "w", encoding="utf-8") as f:
        json.dump(json_data, f, ensure_ascii=False, indent=None, separators=(',', ':'))


emotion_data = parse_markdown_table(md_file)
update_json_with_sentiment(json_file, emotion_data)
