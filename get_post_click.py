"""
Snippet extractor post-click
"""
from playwright.sync_api import sync_playwright
import time

url = "https://www.booking.com/hotel/in/fabexpress-bright-inn.html"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.set_viewport_size({'width': 1920, 'height': 1080})
    
    print(f"Navigating to {url}...")
    page.goto(url, wait_until='domcontentloaded', timeout=60000)
    time.sleep(5)
    
    # Click reviews
    print("Clicking reviews...")
    try:
        page.click('[data-testid="read-all-actionable"], [data-testid="review-score-read-all"], .hp_reviews_count')
        time.sleep(10) # Wait for modal
    except:
        print("Click failed")

    content = page.content()
    with open("post_click_snippet.html", "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Saved {len(content)} bytes to post_click_snippet.html")
    browser.close()
