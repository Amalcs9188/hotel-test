from playwright.sync_api import sync_playwright
import time

def setup_route(page):
    def handle_route(route):
        url = route.request.url
        resource_type = route.request.resource_type
        
        # Log potential blockers
        blocked = False
        if resource_type in ["font", "media"]:
            blocked = True
        elif resource_type == "image" and "bstatic.com" not in url:
            blocked = True
        elif resource_type == "script":
            allowed_domains = ['booking.com', 'bstatic.com', 'maps.googleapis.com']
            if not any(domain in url for domain in allowed_domains):
                blocked = True
        
        if blocked:
            # print(f"BLOCKED [{resource_type}]: {url[:100]}...")
            return route.abort()
        return route.continue_()
    page.route("**/*", handle_route)

def test_blocked_loading():
    url = "https://www.booking.com/hotel/in/the-taj-mahal-palace-mumbai.html"
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            viewport={'width': 1280, 'height': 800}
        )
        page = context.new_page()
        setup_route(page) 
        
        print(f"Navigating to {url}...")
        page.goto(url, wait_until='domcontentloaded')
        
        # Check for WAF
        if page.query_selector('#challenge-container'):
            print("WAF detected, waiting...")
            page.wait_for_selector('#challenge-container', state='hidden', timeout=10000)
            print("WAF cleared!")

        time.sleep(3)
        print("Initial reviews search...")
        initial_count = len(page.query_selector_all('[data-testid="review-card"], .review_item'))
        
        print("Clicking reviews-tab-trigger...")
        trigger = page.query_selector('#reviews-tab-trigger')
        if trigger:
            trigger.click()
            time.sleep(4) # More time
            
        final_count = len(page.query_selector_all('[data-testid="review-card"], .review_item'))
        print(f"Reviews after interaction: {final_count}")

        browser.close()

if __name__ == "__main__":
    test_blocked_loading()
