"""
Advanced selector finder - extracts all possible data from hotel page
"""
from playwright.sync_api import sync_playwright
import time
import json

url = "https://www.booking.com/hotel/in/makam-holiday-home-muzhakkunnu.html"

print(f"🔍 Deep inspection: {url}\n")

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    context = browser.new_context(
        viewport={'width': 1920, 'height': 1080},
        user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    )
    page = context.new_page()
    
    print("📄 Loading page...")
    page.goto(url, wait_until='domcontentloaded', timeout=60000)
    time.sleep(3)
    
    # Use JavaScript to extract all data
    hotel_data = page.evaluate('''() => {
        const data = {
            name: '',
            rating: '',
            address: '',
            description: '',
            amenities: [],
            price: '',
            reviews_count: '',
            all_h1: [],
            all_h2: [],
            all_h3: []
        };
        
        // Get all headings
        document.querySelectorAll('h1').forEach(h => data.all_h1.push(h.textContent.trim()));
        document.querySelectorAll('h2').forEach(h => data.all_h2.push(h.textContent.trim().substring(0, 50)));
        document.querySelectorAll('h3').forEach(h => data.all_h3.push(h.textContent.trim().substring(0, 50)));
        
        // Try to find name
        const h1 = document.querySelector('h1');
        if (h1) data.name = h1.textContent.trim();
        
        // Try to find rating - multiple approaches
        const ratingPatterns = [
            '[data-testid="review-score"]',
            '.bui-review-score__badge',
            '[aria-label*="Scored"]',
            '.review-score-badge'
        ];
        
        for (const pattern of ratingPatterns) {
            const elem = document.querySelector(pattern);
            if (elem) {
                data.rating = elem.textContent.trim();
                break;
            }
        }
        
        // Find address
        const addressPatterns = [
            '[data-testid="address"]',
            '.hp_address_subtitle',
            'span[data-node_tt_id="location_score_tooltip"]'
        ];
        
        for (const pattern of addressPatterns) {
            const elem = document.querySelector(pattern);
            if (elem) {
                data.address = elem.textContent.trim();
                break;
            }
        }
        
        // Find description
        const descPatterns = [
            '[data-testid="property-description"]',
            '#property_description_content',
            '.hp-description'
        ];
        
        for (const pattern of descPatterns) {
            const elem = document.querySelector(pattern);
            if (elem) {
                data.description = elem.textContent.trim().substring(0, 200);
                break;
            }
        }
        
        // Find amenities
        const facilityElems = document.querySelectorAll('[data-testid="facility-group-title"]');
        facilityElems.forEach(elem => {
            data.amenities.push(elem.textContent.trim());
        });
        
        // If no amenities, try alternative
        if (data.amenities.length === 0) {
            document.querySelectorAll('.facilitiesChecklistSection li').forEach(li => {
                data.amenities.push(li.textContent.trim());
            });
        }
        
        // Find price
        const priceElem = document.querySelector('[data-testid="price-and-discounted-price"]') ||
                         document.querySelector('.prco-valign-middle-helper');
        if (priceElem) data.price = priceElem.textContent.trim();
        
        // Find reviews count
        const reviewsElem = document.querySelector('[data-testid="review-score-component"]');
        if (reviewsElem) data.reviews_count = reviewsElem.textContent.trim();
        
        return data;
    }''')
    
    print("\n📊 Extracted Data:\n")
    print(json.dumps(hotel_data, indent=2))
    
    print("\n✅ Complete! Browser will close in 15 seconds...")
    time.sleep(15)
    
    browser.close()

print("\n✅ Done!")
