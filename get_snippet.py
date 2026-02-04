"""
Simple page source extractor
"""
from playwright.sync_api import sync_playwright
import time

url = "https://www.booking.com/hotel/in/makam-holiday-home-muzhakkunnu.html"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True) # Run headless to be safer
    page = browser.new_page()
    try:
        page.goto(url, wait_until='domcontentloaded', timeout=60000)
        time.sleep(5)
        content = page.content()
        print(f"Content length: {len(content)}")
        # Save a snippet
        with open("snippet.html", "w", encoding="utf-8") as f:
            f.write(content)
        print("Snippet saved to snippet.html")
        
        # Try a very simple selector
        name = page.query_selector('h1, h2, span.hp__hotel-name')
        if name:
            print(f"Found name-like element: {name.inner_text()}")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        browser.close()
