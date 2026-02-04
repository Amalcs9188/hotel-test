from playwright.sync_api import sync_playwright
import time

def test_trigger_loading():
    url = "https://www.booking.com/hotel/in/the-taj-mahal-palace-mumbai.html"
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            viewport={'width': 1280, 'height': 800}
        )
        page = context.new_page()
        print(f"Navigating to {url}...")
        try:
            page.goto(url, wait_until='domcontentloaded', timeout=30000)
        except Exception as e:
            print(f"Initial navigation error (expected if redirecting): {e}")
        
        # Check for WAF
        if page.query_selector('#challenge-container'):
            print("WAF detected, waiting...")
            try:
                page.wait_for_selector('#challenge-container', state='hidden', timeout=15000)
                print("WAF cleared!")
            except:
                print("WAF did not clear or redirected.")

        # Wait for page stabilization
        print("Waiting for page to stabilize...")
        time.sleep(3)
        # Re-verify we are on a valid page by looking for property name
        try:
            page.wait_for_selector('[data-testid="property-name"]', timeout=10000)
        except:
            print("Property name not found after wait. Possible block or slow load.")

        initial_count = len(page.query_selector_all('[data-testid="review-card"], .review_item'))
        print(f"Initial reviews: {initial_count}")

        if initial_count == 0:
            print("Looking for reviews-tab-trigger...")
            trigger = page.query_selector('#reviews-tab-trigger')
            if trigger:
                print("trigger found! Clicking...")
                try:
                    trigger.click()
                    print("Clicked! Waiting 2s for load...")
                    time.sleep(2)
                except Exception as e:
                    print(f"Click failed: {e}")
            else:
                print("reviews-tab-trigger NOT found in DOM. Trying alternate: [data-testid='review-score-link']")
                alt_trigger = page.query_selector('[data-testid="review-score-link"], [data-testid="review-score-read-all"]')
                if alt_trigger:
                    print("Alt trigger found! Clicking...")
                    alt_trigger.click()
                    time.sleep(2)
                else:
                    print("No review triggers found.")
                
            final_count = len(page.query_selector_all('[data-testid="review-card"], .review_item'))
            print(f"Reviews after interaction: {final_count}")
            
            if final_count > 0:
                try:
                    review_text = page.query_selector('[data-testid="review-card"] [data-testid="review-title"], .review_item_header_content').inner_text()
                    print(f"Sample review: {review_text[:50]}...")
                except:
                    print("Could not extract sample text from found reviews.")

        browser.close()

if __name__ == "__main__":
    test_trigger_loading()
