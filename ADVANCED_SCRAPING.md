# Advanced Scraping Solutions

This document provides advanced solutions to bypass anti-bot protection and successfully scrape hotel data.

## Solution 1: Selenium with Stealth Mode

### Installation

```bash
pip install selenium-stealth undetected-chromedriver
```

### Implementation

Create `scraper_selenium.py`:

```python
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium_stealth import stealth
import undetected_chromedriver as uc
import time

class SeleniumBookingScraper:
    def __init__(self):
        options = uc.ChromeOptions()
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")

        self.driver = uc.Chrome(options=options)

        # Apply stealth settings
        stealth(self.driver,
            languages=["en-US", "en"],
            vendor="Google Inc.",
            platform="Win32",
            webgl_vendor="Intel Inc.",
            renderer="Intel Iris OpenGL Engine",
            fix_hairline=True,
        )

    def search_hotels(self, city):
        url = f"https://www.booking.com/searchresults.html?ss={city}"
        self.driver.get(url)

        # Wait for hotel cards to load
        wait = WebDriverWait(self.driver, 10)
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "[data-testid='property-card']")))

        # Extract hotel data
        hotels = []
        cards = self.driver.find_elements(By.CSS_SELECTOR, "[data-testid='property-card']")

        for card in cards[:10]:
            try:
                name = card.find_element(By.CSS_SELECTOR, "[data-testid='title']").text
                price = card.find_element(By.CSS_SELECTOR, "[data-testid='price-and-discounted-price']").text
                rating = card.find_element(By.CSS_SELECTOR, "[data-testid='review-score']").text

                hotels.append({
                    "hotel_id": abs(hash(name)) % 100000,
                    "name": name,
                    "price": float(''.join(filter(str.isdigit, price))),
                    "currency": "INR",
                    "rating": float(rating.split()[0]) / 2 if rating else 0.0
                })
            except:
                continue

        return hotels

    def close(self):
        self.driver.quit()
```

## Solution 2: Using ScraperAPI

### Installation

```bash
pip install scraperapi-sdk
```

### Implementation

```python
from scraperapi_sdk import ScraperAPIClient
from bs4 import BeautifulSoup

class ScraperAPIBookingScraper:
    def __init__(self, api_key):
        self.client = ScraperAPIClient(api_key)

    def search_hotels(self, city):
        url = f"https://www.booking.com/searchresults.html?ss={city}"

        # ScraperAPI handles proxies, CAPTCHA, and JavaScript rendering
        response = self.client.get(url, render=True)

        soup = BeautifulSoup(response.text, 'lxml')
        hotel_cards = soup.find_all("div", {"data-testid": "property-card"})

        hotels = []
        for card in hotel_cards[:10]:
            # Parse hotel data (same as before)
            pass

        return hotels
```

**Get API Key**: https://www.scraperapi.com/ (Free tier: 1,000 requests/month)

## Solution 3: Bright Data (Formerly Luminati)

### Installation

```bash
pip install brightdata-sdk
```

### Implementation

```python
from brightdata import BrightDataClient

client = BrightDataClient(
    username='your_username',
    password='your_password',
    zone='residential'
)

proxies = {
    'http': client.get_proxy_url(),
    'https': client.get_proxy_url()
}

response = requests.get(url, proxies=proxies)
```

## Solution 4: Playwright (Better than Selenium)

### Installation

```bash
pip install playwright
playwright install
```

### Implementation

```python
from playwright.sync_api import sync_playwright

def scrape_with_playwright(city):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        )
        page = context.new_page()

        page.goto(f"https://www.booking.com/searchresults.html?ss={city}")
        page.wait_for_selector("[data-testid='property-card']")

        hotels = page.evaluate('''() => {
            const cards = document.querySelectorAll("[data-testid='property-card']");
            return Array.from(cards).slice(0, 10).map(card => ({
                name: card.querySelector("[data-testid='title']")?.textContent,
                price: card.querySelector("[data-testid='price-and-discounted-price']")?.textContent,
                rating: card.querySelector("[data-testid='review-score']")?.textContent
            }));
        }''')

        browser.close()
        return hotels
```

## Comparison

| Solution             | Success Rate   | Speed     | Cost           | Complexity  |
| -------------------- | -------------- | --------- | -------------- | ----------- |
| **Requests + BS4**   | ❌ Low         | ⚡ Fast   | 💰 Free        | ⭐ Easy     |
| **Selenium Stealth** | ✅ Medium      | 🐌 Slow   | 💰 Free        | ⭐⭐ Medium |
| **Playwright**       | ✅ High        | 🚀 Medium | 💰 Free        | ⭐⭐ Medium |
| **ScraperAPI**       | ✅✅ Very High | 🚀 Fast   | 💰💰 $29/mo    | ⭐ Easy     |
| **Bright Data**      | ✅✅✅ Highest | 🚀 Fast   | 💰💰💰 $500/mo | ⭐⭐ Medium |

## Recommendation

**For Development**: Use **Playwright** (free, good success rate)  
**For Production**: Use **ScraperAPI** or **Official APIs** (reliable, legal)

## Quick Start with Playwright

1. Install Playwright:

```bash
pip install playwright
playwright install chromium
```

2. Replace `scraper.py` with Playwright version

3. Test:

```bash
python test_scraper.py
```

This should successfully bypass Booking.com's anti-bot protection! 🎯
