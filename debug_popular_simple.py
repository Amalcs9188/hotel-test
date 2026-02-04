
from playwright.sync_api import sync_playwright
import json
import time

url = "https://www.booking.com/hotel/in/3bhk-villa-10-mins-from-lulu-mall.html"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    try:
        print(f"Loading {url}...")
        page.goto(url, wait_until="domcontentloaded", timeout=60000)
        time.sleep(5)
        
        # Check wrapper
        wrapper = page.query_selector('[data-testid="property-most-popular-facilities-wrapper"]')
        if wrapper:
            print("Wrapper found!")
            print("Wrapper text content:", wrapper.text_content())
            
            # Find sub-elements
            items = wrapper.query_selector_all('[data-testid="facility-item"]')
            print(f"Found {len(items)} items with data-testid='facility-item'")
            for item in items:
                print(f" - Item: {item.text_content().strip()}")
                
            # Try spans if no items
            if len(items) == 0:
                spans = wrapper.query_selector_all('span')
                print(f"Found {len(spans)} spans")
                for span in spans:
                    txt = span.text_content().strip()
                    if txt and txt != "Most popular facilities":
                        print(f" - Span: {txt}")
        else:
            print("Wrapper NOT found!")
            # Check for alternative
            alt = page.query_selector('.hp_desc_important_facilities')
            if alt:
                print("Alternative (.hp_desc_important_facilities) found!")
                print(alt.text_content())
            
    except Exception as e:
        print(f"Error: {e}")
    finally:
        browser.close()
