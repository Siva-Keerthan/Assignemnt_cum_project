from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import os
import requests
import pandas as pd
from PIL import Image

# Configurations
NUM_IMAGES = 50  # Number of images per category
SAVE_FOLDER = "dataset"
CATEGORIES = [
    "Cars", "Dogs", "Landmarks", "Fruits", "Flowers", "Birds", "Airplanes", "Cats", "Trees", "Motorcycles",
    "Buildings", "Insects", "Electronic Gadgets", "Bridges", "Mountains", "Sports Equipment", "Food Items",
    "Musical Instruments", "Animals", "Ships"
]

# Set up Selenium WebDriver (Ensure chromedriver is installed)
options = webdriver.ChromeOptions()
options.add_argument("--headless")  # Run in headless mode
options.add_argument("--disable-gpu")
driver = webdriver.Chrome(options=options)

# Function to download images
def download_image(url, filepath):
    try:
        response = requests.get(url, stream=True, timeout=5)
        if response.status_code == 200:
            with open(filepath, 'wb') as file:
                for chunk in response.iter_content(1024):
                    file.write(chunk)
            return True
    except Exception as e:
        print(f"Failed to download {url}: {e}")
    return False

# Metadata storage
metadata = []

# Start downloading images
for category in CATEGORIES:
    search_url = f"https://www.google.com/search?q={category}&tbm=isch"
    driver.get(search_url)
    time.sleep(2)
    
    # Scroll down to load more images
    body = driver.find_element(By.TAG_NAME, 'body')
    for _ in range(5):  # Scroll multiple times
        body.send_keys(Keys.END)
        time.sleep(2)
    
    # Find image elements
    images = driver.find_elements(By.CSS_SELECTOR, "img")
    os.makedirs(f"{SAVE_FOLDER}/{category}", exist_ok=True)
    
    count = 0
    for img in images:
        if count >= NUM_IMAGES:
            break
        
        try:
            img_url = img.get_attribute("src")
            if img_url and img_url.startswith("http"):
                filename = f"{SAVE_FOLDER}/{category}/{category}_{count}.jpg"
                if download_image(img_url, filename):
                    try:
                        with Image.open(filename) as img_file:
                            width, height = img_file.size
                            resolution = f"{width}x{height}"
                    except Exception:
                        resolution = "Unknown"
                    metadata.append([category, img_url, filename, resolution])
                    count += 1
        except Exception as e:
            print(f"Skipping image: {e}")

# Save metadata to CSV
pd.DataFrame(metadata, columns=["Category", "URL", "Filename", "Resolution"]).to_csv("image_metadata.csv", index=False)

driver.quit()
print("Image collection completed!")

