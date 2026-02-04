
from playwright.sync_api import sync_playwright
import time

url = "https://www.booking.com/hotel/in/sofitel-mumbai-bkc.html"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(
        user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    )
    
    print(f"Navigating to {url}...")
    page.goto(url, wait_until='domcontentloaded')
    
    # Wait for reviews to potentially load
    time.sleep(3)
    
    # Dump review card HTML
    review_html = page.evaluate('''() => {
        const sel = '[data-testid="review-card"], [data-testid="featuredreview"], .review_item, .c-review-block';
        const el = document.querySelector(sel);
        return el ? el.outerHTML : "NOT FOUND";
    }''')
    
    with open("review_debug.html", "w", encoding="utf-8") as f:
        f.write(review_html)
    
    print("Saved review HTML to review_debug.html")
    browser.close()
