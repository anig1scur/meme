import os
import json
import requests
from bs4 import BeautifulSoup
import pandas as pd


BASE = os.path.join(os.path.dirname(__file__), "../public/top")

input_csv = os.path.join(BASE, "memes.csv")
IMG_DIR = os.path.join(BASE, "images")
OUTPUT_JSON = os.path.join(BASE, "meme_details.json")


def scrape_meme_details(meme_name, url):
    print(f"Scraping details for {meme_name}")
    print(f"URL: {url}")
    # Scrape image
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    # Scrape image
    img_url = soup.select_one("header > a > img")["src"]

    # Initialize variables
    meme_id = url.split("/")[-1]
    meme_type = None
    year = None
    origin = None

    # Find the <dl> section containing the details
    details_dl = soup.select_one("#entry_body > aside > dl")

    # Iterate through <dt> and <dd> pairs
    for dt, dd in zip(details_dl.find_all("dt"), details_dl.find_all("dd")):
        # Check for Type
        if "Type" in dt.text:
            meme_type = dd.text.strip()
        # Check for Year
        elif "Year" in dt.text:
            year = dd.text.strip()
        # Check for Origin
        elif "Origin" in dt.text:
            origin = dd.text.strip()

    # h2 #about
    about = None
    about_el = soup.select_one("#about")
    if about_el:
        about = about_el.find_next("p").text.strip()

    origin_story = None
    origin_el = soup.select_one("#origin")
    if origin_el:
        origin_story = origin_el.find_next("p").text.strip()

    # Download image and save it locally
    img_response = requests.get(img_url)
    img_name = f"{meme_id}.jpg"
    file_path = os.path.join(IMG_DIR, img_name)
    if os.path.exists(file_path):
        print(f"Image {img_name} already exists. Skipping download.")
        return meme_name, img_name, meme_type, year, origin, about, origin_story

    with open(os.path.join(IMG_DIR, img_name), "wb") as img_file:
        img_file.write(img_response.content)

    return meme_name, img_name, meme_type, year, origin, about, origin_story


df = pd.read_csv(input_csv)
meme_data = []

# Scrape details for each meme
for index, row in df.iterrows():
    meme_name = row["title"]
    url = row["kym_url"]
    imgflip_url = row["url"]
    # id,title,url,kym_url
    details = scrape_meme_details(meme_name, url)
    meme_data.append(
        {
            "name": details[0],
            "image": details[1],
            "type": details[2],
            "year": details[3],
            "origin": details[4],
            "about": details[5],
            "origin_story": details[6],
            "link": url,
            "imgflip": imgflip_url,
        }
    )

# Save the data to a JSON file
with open(OUTPUT_JSON, "w", encoding="utf-8") as json_file:
    json.dump(meme_data, json_file, ensure_ascii=False, indent=4)

print("Scraping and saving to meme_details.json completed")
