import requests
from bs4 import BeautifulSoup
import csv
import os

BASE_URL = "https://imgflip.com/memetemplates?sort=top-all-time&page="
HEADERS = {"User-Agent": "Mozilla/5.0"}
OUTPUT_FILE = os.path.join(os.path.dirname(__file__), "../data/imgflip/memes.csv")


# Function to scrape a single page
def scrape(page_num):
    url = BASE_URL + str(page_num)
    response = requests.get(url, headers=HEADERS)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    memes = []

    for box in soup.select(".mt-box"):
        title_tag = box.select_one(".mt-title a")
        img_tag = box.select_one(".mt-img-wrap img")

        if title_tag and img_tag:
            meme_url = title_tag["href"]
            meme_id = meme_url.split("/")[-1]
            title = title_tag["title"].replace(" Meme", "")
            memes.append([meme_id, title, "http://imgflip.com" + meme_url])

    return memes


# Scrape multiple pages
def main(pages=10):
    all_memes = []
    for i in range(1, pages + 1):
        print(f"Scraping page {i}...")
        all_memes.extend(scrape(i))

    # Save to CSV
    with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["id", "title", "url"])
        writer.writerows(all_memes)

    print(f"Scraping completed! Data saved to {OUTPUT_FILE}")


# Run the scraper
if __name__ == "__main__":
    main(10)
