import os
import requests
from bs4 import BeautifulSoup
import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import string

nltk.download('stopwords')
nltk.download('punkt')

# Define 20 categories and their corresponding websites
categories = {
    "Technology": ["https://techcrunch.com", "https://www.theverge.com", "https://www.wired.com"],
    "Science": ["https://www.sciencedaily.com", "https://www.livescience.com", "https://www.nature.com"],
    "Sports": ["https://www.espn.com", "https://www.sportskeeda.com", "https://www.skysports.com"],
    "Health": ["https://www.webmd.com", "https://www.medicalnewstoday.com", "https://www.healthline.com"],
    "Business": ["https://www.forbes.com", "https://www.businessinsider.com", "https://www.cnbc.com"],
    "Education": ["https://www.edutopia.org", "https://www.education.com", "https://www.timeshighereducation.com"],
    "Entertainment": ["https://www.rollingstone.com", "https://www.billboard.com", "https://www.hollywoodreporter.com"],
    "Politics": ["https://www.politico.com", "https://www.bbc.com/news/politics", "https://www.nytimes.com/section/politics"],
    "Finance": ["https://www.marketwatch.com", "https://www.fool.com", "https://www.investopedia.com"],
    "Environment": ["https://www.nationalgeographic.com", "https://www.worldwildlife.org", "https://www.climatecentral.org"],
    "Automobile": ["https://www.caranddriver.com", "https://www.autoblog.com", "https://www.motortrend.com"],
    "Gaming": ["https://www.ign.com", "https://www.pcgamer.com", "https://www.gamespot.com"],
    "Fashion": ["https://www.vogue.com", "https://www.elle.com", "https://www.gq.com"],
    "Travel": ["https://www.lonelyplanet.com", "https://www.cntraveler.com", "https://www.travelandleisure.com"],
    "Food": ["https://www.foodnetwork.com", "https://www.seriouseats.com", "https://www.epicurious.com"],
    "History": ["https://www.history.com", "https://www.britannica.com", "https://www.smithsonianmag.com/history"],
    "Artificial Intelligence": ["https://www.aitrends.com", "https://www.analyticsvidhya.com", "https://www.deeplearning.ai"],
    "Cybersecurity": ["https://www.cybersecurity-insiders.com", "https://www.darkreading.com", "https://www.csoonline.com"],
    "Startups": ["https://www.startupgrind.com", "https://www.angel.co", "https://www.ycombinator.com"],
    "Space Exploration": ["https://www.nasa.gov", "https://www.spacex.com", "https://www.esa.int"],
}

# Function to clean text
def clean_text(text):
    text = re.sub(r'<.*?>', '', text)  # Remove HTML tags
    text = text.translate(str.maketrans('', '', string.punctuation))  # Remove punctuation
    words = word_tokenize(text.lower())  # Tokenize and convert to lowercase
    words = [word for word in words if word not in stopwords.words('english') and word.isalpha()]  # Remove stopwords
    return ' '.join(words)

# Create a directory to store text files
if not os.path.exists("text_datasets"):
    os.makedirs("text_datasets")

# Scraping function
def scrape_text(category, urls):
    all_text = ""
    for url in urls:
        try:
            response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
            soup = BeautifulSoup(response.text, "html.parser")
            
            # Extract text from paragraphs
            paragraphs = soup.find_all("p")
            content = '\n'.join([para.get_text() for para in paragraphs])
            clean_content = clean_text(content)
            all_text += clean_content + "\n\n"
        except Exception as e:
            print(f"Error scraping {url}: {e}")
    
    # Save text to a file
    with open(f"text_datasets/{category}.txt", "w", encoding="utf-8") as file:
        file.write(all_text)
    print(f"Saved text data for {category}")

# Run the scraper for each category
for category, urls in categories.items():
    scrape_text(category, urls)
