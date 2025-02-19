import json
import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager


BASE = os.path.join(os.path.dirname(__file__), "../public")


def load_json(filename):
    with open(filename, "r", encoding="utf-8") as file:
        return json.load(file)


def save_json(filename, data):
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)


options = webdriver.ChromeOptions()
# options.binary_location = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

options.add_experimental_option(
    "prefs",
    {
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing.enabled": True,
        "profile.default_content_setting_values.automatic_downloads": 1,
        "download.default_directory": "/Users/ac3r/Downloads/",
    },
)
options.add_argument("--disable-blink-features=AutomationControlled")


# options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument("--window-size=1920,1080")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
# options.add_argument(
#     "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
# )


driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()), options=options
)
driver.execute_script(
    "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
)

json_file = os.path.join(BASE, "meme_details.json")
data = load_json(json_file)

for item in data:
    query = item["name"]
    id = item["image"].split(".")[0]
    csv_filename = f"{id}.csv"
    file_path = os.path.join(BASE, "top50/trending/", csv_filename)
    if os.path.exists(file_path):
        print(f"CSV file {csv_filename} already exists. Skipping download.")
        continue

    search_url = f"https://trends.google.com/trends/explore?date=all&q={query.replace(' ', '%20')}"

    driver.get(search_url)
    time.sleep(3)

    try:
        export_button = driver.find_element(By.CLASS_NAME, "widget-actions-item")
        if not export_button:
            # refresh and Try again
            driver.refresh()
            time.sleep(1)
            export_button = driver.find_element(By.CLASS_NAME, "widget-actions-item")
        export_button.click()
        time.sleep(2)

        os.rename("/Users/ac3r/Downloads/multiTimeline.csv", file_path)

        item["csv_file"] = csv_filename
    except Exception as e:
        print(f"Error processing {query}: {e}")

driver.quit()
save_json(json_file, data)
