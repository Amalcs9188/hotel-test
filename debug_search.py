"""
Debug script to test hotel search and URL extraction
"""
from playwright.sync_api import sync_playwright
import time

city = "Kochi"
url = f"https://www.booking.com/searchresults.html?ss={city}&checkin=2026-02-11&checkout=2026-02-12&group_adults=2&group_children=0&no_rooms=1"

with sync_playwright() as p:
    browser = p.chromium.launch(
        headless=True,
        args=['--disable-blink-features=AutomationControlled']
    )
    context = browser.new_context(
        viewport={'width': 1920, 'height': 1080},
        user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        locale='en-US'
    )
    page = context.new_page()
    
    print(f"Navigating to: {url}")
    page.goto(url, wait_until='domcontentloaded', timeout=60000)
    
    # Wait for cards
    try:
        page.wait_for_selector('[data-testid="property-card"]', timeout=15000)
        print("[OK] Property cards loaded")
    except:
        print("[FAIL] Property cards not found, trying alternative")
        page.wait_for_selector('.sr_item', timeout=10000)
    
    time.sleep(2)
    
    # Debug: Check what selectors exist
    result = page.evaluate('''() => {
        const cards = document.querySelectorAll('[data-testid="property-card"]');
        console.log(`Found ${cards.length} property cards`);
        
        if (cards.length === 0) return { error: "No cards found" };
        
        const firstCard = cards[0];
        
        // Test all possible link selectors
        const linkTests = {
            'a[data-testid="title-link"]': firstCard.querySelector('a[data-testid="title-link"]'),
            'a[href*="/hotel/"]': firstCard.querySelector('a[href*="/hotel/"]'),
            'a.e13098a59f': firstCard.querySelector('a.e13098a59f'),
            'h3 a': firstCard.querySelector('h3 a'),
            'a[aria-label]': firstCard.querySelector('a[aria-label]'),
            '[data-testid="title"] a': firstCard.querySelector('[data-testid="title"] a'),
            'a': firstCard.querySelectorAll('a').length
        };
        
        const results = {};
        for (const [selector, elem] of Object.entries(linkTests)) {
            if (typeof elem === 'number') {
                results[selector] = `${elem} links found`;
            } else if (elem) {
                results[selector] = {
                    found: true,
                    href: elem.getAttribute('href'),
                    text: elem.textContent.trim().substring(0, 50)
                };
            } else {
                results[selector] = { found: false };
            }
        }
        
        // Get all links in first card
        const allLinks = [];
        firstCard.querySelectorAll('a').forEach((a, i) => {
            if (i < 5) {
                allLinks.push({
                    href: a.getAttribute('href'),
                    text: a.textContent.trim().substring(0, 30),
                    hasHotel: a.getAttribute('href')?.includes('/hotel/')
                });
            }
        });
        
        return {
            cardCount: cards.length,
            linkTests: results,
            allLinks: allLinks
        };
    }''')
    
    print("\n=== DEBUG RESULTS ===")
    import json
    output = json.dumps(result, indent=2)
    print(output)
    
    with open("debug_output.json", "w") as f:
        f.write(output)
    print("\nSaved to debug_output.json")
    
    browser.close()
