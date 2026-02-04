
from playwright.sync_api import sync_playwright
import time

url = "https://www.booking.com/hotel/in/the-taj-mahal-palace-mumbai.html"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    # Set locale and cookies to force English
    context = browser.new_context(
        user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        viewport={'width': 1280, 'height': 2000},
        locale='en-US',
        extra_http_headers={'Accept-Language': 'en-US,en;q=0.9'}
    )
    page = context.new_page()
    
    # Add cookie to force English
    context.add_cookies([{
        'name': 'booking_lang',
        'value': 'en-us',
        'domain': '.booking.com',
        'path': '/'
    }])
    
    print(f"Navigating to {url}...")
    page.goto(url, wait_until='domcontentloaded')
    time.sleep(5)
    
    # Capture review metadata details
    review_info = page.evaluate('''() => {
        const results = [];
        const selectors = ['[data-testid="review-card"]', '[data-testid="featuredreview"]', '.review_item', '.c-review-block'];
        
        selectors.forEach(sel => {
            document.querySelectorAll(sel).forEach(el => {
                results.push({
                    selector: sel,
                    html: el.outerHTML,
                    text: el.innerText,
                    author_candidates: Array.from(el.querySelectorAll('h4, span, div')).map(e => ({tag: e.tagName, text: e.innerText, testid: e.getAttribute('data-testid')})),
                    score_candidates: Array.from(el.querySelectorAll('div, span')).filter(e => e.innerText && /^\\d+(\\.\\d+)?$/.test(e.innerText.trim())).map(e => ({tag: e.tagName, text: e.innerText, testid: e.getAttribute('data-testid'), class: e.className}))
                });
            });
        });
        return results;
    }''')
    
    import json
    with open("review_metadata_debug.json", "w", encoding="utf-8") as f:
        json.dump(review_info, f, indent=2)
    
    print(f"Captured {len(review_info)} review cards to review_metadata_debug.json")
    browser.close()
