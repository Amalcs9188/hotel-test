"""
Targeted debug for children of popular facilities wrapper
"""
from playwright.sync_api import sync_playwright
import time
import json

url = "https://www.booking.com/hotel/in/3bhk-villa-10-mins-from-lulu-mall.html"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto(url, wait_until='domcontentloaded')
    time.sleep(3)
    
    result = page.evaluate('''() => {
        const wrapper = document.querySelector('[data-testid="property-most-popular-facilities-wrapper"]');
        if (!wrapper) return "Wrapper not found";
        
        const childrenInfo = [];
        // Look for items that look like facility names
        const items = wrapper.querySelectorAll('span, div, li');
        items.forEach(el => {
            const text = el.textContent.trim();
            if (text && text.length > 0 && text !== 'Most popular facilities' && !text.includes('Most popular facilities')) {
                // Only take leaf nodes or nodes with specific classes/testids
                if (el.children.length === 0 || el.getAttribute('data-testid') === 'facility-item') {
                    childrenInfo.push({
                        text: text,
                        tag: el.tagName,
                        testid: el.getAttribute('data-testid'),
                        className: el.className
                    });
                }
            }
        });
        
        return childrenInfo;
    }''')
    
    print(json.dumps(result, indent=2))
    browser.close()
