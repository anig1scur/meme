import os
import csv
import requests
from bs4 import BeautifulSoup
import urllib.parse


def fetch_kym_url(title):
    search_url = f"https://knowyourmeme.com/search?q={urllib.parse.quote(title)}"
    response = requests.get(search_url, headers={"User-Agent": "Mozilla/5.0"})
    if response.status_code != 200:
        print(f"Failed to fetch: {search_url}")
        return None

    soup = BeautifulSoup(response.text, "html.parser")
    link = soup.find("a", class_="item")
    if not link:
        print(f"No result found for: {title}")
        return None

    return link["href"] if link else None


def process_csv(input_file, output_file):
    with open(input_file, newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        fieldnames = reader.fieldnames + ["kym_url"]
        rows = list(reader)

    for row in rows:
        title = row["Title"]
        row["kym_url"] = fetch_kym_url(title)

    with open(output_file, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


INPUT_FILE = os.path.join(os.path.dirname(__file__), "../data/imgflip/memes.csv")
OUTPUT_FILE = os.path.join(os.path.dirname(__file__), "../data/knowyourmeme/memes.csv")


if __name__ == "__main__":
    process_csv(INPUT_FILE, OUTPUT_FILE)
