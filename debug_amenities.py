"""
Robust debug script to find the correct selector for popular facilities
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
    
    page.add_init_script("""
        Object.defineProperty(navigator, 'webdriver', {
            get: () => undefined
        });
    """)
    
    print(f"Navigating to: {url}")
    try:
        # Using domcontentloaded is faster and safer against background noise
        page.goto(url, wait_until='domcontentloaded', timeout=30000)
        print("Page loaded (DOM content).")
        # Explicit wait for some key elements
        page.wait_for_selector('h2', timeout=10000)
        time.sleep(3) # Let JS settle
    except Exception as e:
        print(f"Navigation error: {e}")
    
    # Comprehensive search for popular facilities
    result = page.evaluate('''() => {
        const results = {
            selectorsFound: {},
            potentialSections: []
        };
        
        const selectors = [
            '.important_facility',
            '.hp_facility_list li',
            '[data-testid="property-most-popular-facilities-wrapper"]',
            '[data-testid="property-most-popular-facilities-wrapper"] [data-testid="facility-item"]',
            '.hp-most-popular-facilities li',
            '.property-highlights li',
            '[data-testid="facility-group"]',
            '.hp_desc_important_facilities li',
            '[data-testid="property-highlights"]',
            '.hp-most-popular-facilities'
        ];
        
        selectors.forEach(s => {
            const elements = document.querySelectorAll(s);
            if (elements.length > 0) {
                results.selectorsFound[s] = {
                    count: elements.length,
                    samples: Array.from(elements).slice(0, 5).map(el => el.textContent.trim())
                };
            }
        });
        
        // Find text content matches
        const allText = document.body.innerText;
        results.hasPopularFacilitiesText = allText.includes('Most popular facilities');
        
        // Search by text "Most popular facilities"
        const headings = Array.from(document.querySelectorAll('h1, h2, h3, h4, h5, span, div'));
        const popularHeading = headings.find(el => el.textContent.includes('Most popular facilities'));
        if (popularHeading) {
            results.popularHeadingPath = 'Found heading, checking siblings/parent';
            const parent = popularHeading.parentElement;
            results.parentText = parent.textContent.trim().substring(0, 200);
            results.parentClasses = parent.className;
            
            // Look for icons/text nearby
            const nearbyItems = Array.from(parent.querySelectorAll('li, div[data-testid="facility-item"], div.b43e553776'));
            results.nearbyItems = nearbyItems.slice(0, 10).map(el => el.textContent.trim()).filter(t => t.length > 0 && t.length < 50);
        }
        
        return results;
    }''')
    
    print("\n=== SELECTOR ANALYSIS ===")
    import json
    print(json.dumps(result, indent=2))
    
    browser.close()
