"""
Snippet extractor for problematic hotel page
"""
from playwright.sync_api import sync_playwright
import time

url = "https://www.booking.com/hotel/in/fabexpress-bright-inn.html"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    context = browser.new_context(
        viewport={'width': 1920, 'height': 1080},
        user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        locale='en-US'
    )
    page = context.new_page()
    try:
        print(f"Navigating to {url}...")
        page.goto(url, wait_until='domcontentloaded', timeout=60000)
        time.sleep(10) # Give it plenty of time for background content
        
        # Scroll down to trigger lazy loading of amenities/reviews if needed
        page.evaluate("window.scrollTo(0, document.body.scrollHeight / 2)")
        time.sleep(2)
        page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        time.sleep(2)
        
        content = page.content()
        with open("problem_snippet.html", "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Saved {len(content)} bytes to problem_snippet.html")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        browser.close()
