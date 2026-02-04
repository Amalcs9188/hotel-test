"""
Debug script to check review selectors on hotel details page
"""
from playwright.sync_api import sync_playwright
import time

url = "https://www.booking.com/hotel/in/3bhk-villa-10-mins-from-lulu-mall.html"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    context = browser.new_context(
        viewport={'width': 1920, 'height': 1080},
        user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
        locale='en-US'
    )
    page = context.new_page()
    
    print(f"Navigating to: {url}")
    page.goto(url, wait_until='domcontentloaded', timeout=60000)
    
    # Wait for content
    try:
        page.wait_for_selector('h1, h2, [data-testid="property-name"]', timeout=10000)
    except:
        pass
    
    # Scroll to load reviews
    print("Scrolling to load content...")
    for i in range(1, 4):
        page.evaluate(f"window.scrollTo(0, {i * 1500})")
        time.sleep(1.0)
    page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
    time.sleep(2.0)
    
    # Check all review selectors
    result = page.evaluate('''() => {
        const selectors = [
            '[data-testid="review-card"]',
            '.review_item',
            '.c-review-block',
            '.featured_review',
            '.review_list_new_item_block',
            '[data-testid="review-author-name"]',
            '.review-card',
            '[data-testid="reviews-container"]'
        ];
        
        const results = {};
        for (const selector of selectors) {
            const elements = document.querySelectorAll(selector);
            results[selector] = elements.length;
        }
        
        // Check for review buttons/links
        const reviewButtons = [
            '[data-testid="read-all-actionable"]',
            '[data-testid="review-score-read-all"]',
            '.hp_reviews_count',
            '#show_reviews_tab',
            'a[href*="reviews"]'
        ];
        
        results['buttons'] = {};
        for (const selector of reviewButtons) {
            const elem = document.querySelector(selector);
            results['buttons'][selector] = elem ? 'FOUND' : 'NOT FOUND';
        }
        
        // Check for review score
        const scoreElem = document.querySelector('[data-testid="review-score-component"]');
        results['hasReviewScore'] = scoreElem ? scoreElem.textContent.trim() : 'NOT FOUND';
        
        return results;
    }''')
    
    print("\n=== REVIEW SELECTOR RESULTS ===")
    import json
    print(json.dumps(result, indent=2))
    
    # Try clicking review button if found
    print("\n=== ATTEMPTING TO LOAD REVIEWS ===")
    try:
        for selector in ['[data-testid="read-all-actionable"]', '[data-testid="review-score-read-all"]', 'a[href*="reviews"]']:
            elem = page.query_selector(selector)
            if elem:
                print(f"Found button: {selector}")
                elem.scroll_into_view_if_needed()
                elem.click(force=True)
                print("Clicked! Waiting for reviews to load...")
                time.sleep(3)
                
                # Check again
                review_count = page.evaluate('''() => {
                    return document.querySelectorAll('[data-testid="review-card"], .review_item, .c-review-block').length;
                }''')
                print(f"Reviews found after click: {review_count}")
                break
    except Exception as e:
        print(f"Error clicking: {e}")
    
    browser.close()
