from playwright.sync_api import sync_playwright
import time

def dump_html_and_find_reviews():
    url = "https://www.booking.com/hotel/in/the-taj-mahal-palace-mumbai.html"
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            viewport={'width': 1280, 'height': 800},
            locale='en-US'
        )
        page = context.new_page()
        page.add_init_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        
        print(f"Navigating to {url}...")
        page.goto(url, wait_until='domcontentloaded', timeout=40000)
        
        # Check for WAF
        if page.query_selector('#challenge-container'):
            print("WAF detected, waiting...")
            try:
                page.wait_for_selector('#challenge-container', state='hidden', timeout=15000)
                print("WAF cleared!")
            except:
                print("WAF did not clear.")
        
        # Wait for core content
        page.wait_for_selector('[data-testid="property-name"], h1, h2', timeout=5000)
        
        print("Scrolling down to trigger lazy loads...")
        for i in range(1, 4):
            page.evaluate(f"window.scrollTo(0, {i * 1000})")
            time.sleep(0.5)
            
        time.sleep(1.5)
        
        # Take screenshot
        page.screenshot(path="full_page_debug.png", full_page=True)
        
        # Check review elements count
        res = page.evaluate('''() => {
            const sels = ['[data-testid="review-card"]', '.review_item', '.c-review-block', '.featured_review'];
            const counts = {};
            sels.forEach(s => counts[s] = document.querySelectorAll(s).length);
            return counts;
        }''')
        print(f"Review element counts: {res}")
        
        # Save HTML
        with open("full_dom.html", "w", encoding="utf-8") as f:
            f.write(page.content())
            
        browser.close()

if __name__ == "__main__":
    dump_html_and_find_reviews()
