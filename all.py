import json
import time
import pandas as pd
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

class WebScraper:
    def __init__(self):
        options = Options()
        # options.add_argument("--headless") # Uncomment to run in background
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        self.wait = WebDriverWait(self.driver, 10)
        self.data = {"reviews": [], "products": [], "testimonials": []}

    def scrape_reviews(self):
        print("Scraping Reviews (with 'Load More')...")
        self.driver.get("https://web-scraping.dev/reviews")
        
        # Click 'Load More' 3 times to get a representative dataset
        for _ in range(3):
            try:
                btn = self.wait.until(EC.element_to_be_clickable((By.ID, "page-load-more")))
                self.driver.execute_script("arguments[0].click();", btn)
                time.sleep(1.5)
            except:
                break

        cards = self.driver.find_elements(By.CLASS_NAME, "review")
        for card in cards:
            date_raw = card.find_element(By.CSS_SELECTOR, '[data-testid="review-date"]').text
            text = card.find_element(By.CSS_SELECTOR, '[data-testid="review-text"]').text
            self.data["reviews"].append({
                "date": datetime.strptime(date_raw.strip(), '%Y-%m-%d').isoformat(),
                "content": text.strip()
            })

    def scrape_products(self):
        print("Scraping Products (5 Pages)...")
        for page in range(1, 6):
            self.driver.get(f"https://web-scraping.dev/products?page={page}")
            time.sleep(1.5)
            cards = self.driver.find_elements(By.CLASS_NAME, "product")
            for card in cards:
                title = card.find_element(By.CSS_SELECTOR, "h3.mb-0 a").text.strip()
                price = card.find_element(By.CLASS_NAME, "price").text.strip()
                self.data["products"].append({"title": title, "price": price})

    def scrape_testimonials(self):
        print("Scraping Testimonials (Infinite Scroll)...")
        self.driver.get("https://web-scraping.dev/testimonials")
        
        last_height = self.driver.execute_script("return document.body.scrollHeight")
        while True:
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
            new_height = self.driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height: break
            last_height = new_height

        cards = self.driver.find_elements(By.CLASS_NAME, "testimonial")
        for card in cards:
            text = card.find_element(By.CLASS_NAME, "text").text.strip()
            user = card.find_element(By.TAG_NAME, "identicon-svg").get_attribute("username")
            self.data["testimonials"].append({"user": user, "text": text})

    def save_and_close(self):
        with open('combined_data.json', 'w', encoding='utf-8') as f:
            json.dump(self.data, f, indent=4, ensure_ascii=False)
        self.driver.quit()
        print(f"\nSUCCESS! Scraped:")
        print(f"- {len(self.data['reviews'])} Reviews")
        print(f"- {len(self.data['products'])} Products")
        print(f"- {len(self.data['testimonials'])} Testimonials")

if __name__ == "__main__":
    scraper = WebScraper()
    scraper.scrape_reviews()
    scraper.scrape_products()
    scraper.scrape_testimonials()
    scraper.save_and_close()