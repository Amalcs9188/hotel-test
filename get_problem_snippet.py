
from playwright.sync_api import sync_playwright
import time

url = "https://www.booking.com/hotel/in/taj-mahal-palace.html"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(
        user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36'
    )
    print(f"Navigating to {url}...")
    page.goto(url, timeout=60000)
    
    # Wait a bit
    time.sleep(5)
    
    print("Page Title:", page.title())
    
    # Check H1
    h1s = page.query_selector_all('h1')
    print(f"Found {len(h1s)} H1 elements:")
    for h in h1s:
        print(f" - {h.text_content().strip()}")
        
    # Check H2
    h2s = page.query_selector_all('h2')
    print(f"Found {len(h2s)} H2 elements:")
    for i, h in enumerate(h2s):
        print(f" - {i}: {h.text_content().strip()} (Classes: {h.get_attribute('class')})")
        if i >= 10: break

    # Check specific selectors
    print("\nChecking specific selectors:")
    selectors = [
        'h2[data-testid="property-name"]',
        '.pp-header__title',
        '.hp__hotel-name',
        '#hp_hotel_name',
        '[data-testid="title"]'
    ]
    for s in selectors:
        el = page.query_selector(s)
        print(f" - {s}: {'FOUND: ' + el.text_content().strip() if el else 'NOT FOUND'}")

    # Check JSON-LD
    scripts = page.query_selector_all('script[type="application/ld+json"]')
    print(f"\nFound {len(scripts)} JSON-LD scripts")
    
    # Save HTML
    with open("problem_snippet.html", "w", encoding="utf-8") as f:
        f.write(page.content())
    print("\nSaved HTML to problem_snippet.html")

    browser.close()
