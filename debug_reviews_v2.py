from playwright.sync_api import sync_playwright
import time
import json

def debug_reviews_extreme():
    url = "https://www.booking.com/hotel/in/the-taj-mahal-palace-mumbai.html"
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            viewport={'width': 1280, 'height': 800},
            locale='en-US',
            timezone_id='Asia/Kolkata'
        )
        page = context.new_page()
        page.add_init_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        
        print(f"Navigating to {url}...")
        page.goto(url, wait_until='domcontentloaded', timeout=40000)
        
        # WAF Check
        if page.query_selector('#challenge-container'):
            try:
                page.wait_for_selector('#challenge-container', state='hidden', timeout=15000)
                print("WAF cleared!")
            except:
                print("WAF did not clear.")
        
        # Wait for core content
        page.wait_for_selector('[data-testid="property-name"], h1, h2', timeout=10000)
        
        # Click the reviews link/button
        print("Looking for reviews button...")
        # Common selectors for the review score button that opens the overlay
        selectors = [
            '[data-testid="review-score-link"]',
            '[data-testid="review-score-read-all"]',
            '.hp_reviews_count',
            '#show_reviews_tab',
            'text="reviews"',
            'text="Wonderful"'
        ]
        
        for s in selectors:
            try:
                btn = page.query_selector(s)
                if btn:
                    print(f"Found button with selector '{s}'. Clicking...")
                    btn.click()
                    # Wait for review modal or section
                    page.wait_for_selector('[data-testid="review-card"], .review_item, .c-review-block, [data-testid="review-author-name"]', timeout=10000)
                    print("Reviews loaded successfully via click!")
                    break
            except Exception as e:
                print(f"Click with '{s}' failed: {e}")
        
        # Now extract a few reviews to see their structure
        reviews = page.evaluate('''() => {
            const results = [];
            const cards = document.querySelectorAll('[data-testid="review-card"], .review_item, .c-review-block');
            cards.forEach((card, i) => {
                if (i >= 3) return;
                results.push({
                    index: i,
                    text: card.innerText.substring(0, 200),
                    author: card.querySelector('[data-testid="review-author-name"], .bui-avatar-block__title, .review_item_reviewer_name')?.innerText || 'NOT FOUND',
                    score: card.querySelector('[data-testid="review-score-badge"], .bui-review-score__badge, .review-score-badge')?.innerText || 'NOT FOUND',
                    comment: card.querySelector('[data-testid="review-positive-text"], [data-testid="review-title"], .review_item_header_content, .c-review-block__title')?.innerText || 'NOT FOUND'
                });
            });
            return results;
        }''')
        
        print(f"Extracted {len(reviews)} review samples:")
        print(json.dumps(reviews, indent=2))
        
        # If still 0, dump all text in the body to see if we missed them
        if len(reviews) == 0:
            print("Zero reviews found. Dumping body text snippet...")
            body_text = page.evaluate('() => document.body.innerText.substring(0, 1000)')
            print(f"Body text start: {body_text}")
            page.screenshot(path="debug_reviews_fail.png")

        browser.close()

if __name__ == "__main__":
    debug_reviews_extreme()
