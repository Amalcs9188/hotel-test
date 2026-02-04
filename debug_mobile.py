
import asyncio
from playwright.sync_api import sync_playwright
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def debug_mobile_details():
    hotel_url = "https://www.booking.com/hotel/in/3bhk-villa-10-mins-from-lulu-mall.html"
    
    with sync_playwright() as p:
        logger.info("Starting browser...")
        browser = p.chromium.launch(headless=True)
        
        # Desktop User Agent
        context = browser.new_context(
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
            viewport={'width': 1280, 'height': 800}
        )
        page = context.new_page()
        
        # Blockers
        def handle_route(route):
            if route.request.resource_type in ["font", "media"]:
                return route.abort()
            return route.continue_()
        
        # page.route("**/*", handle_route)
        
        logger.info(f"Navigating to {hotel_url}...")
        page.goto(hotel_url, wait_until='networkidle', timeout=60000)
        
        # Check if name is visible
        name = page.evaluate('document.querySelector("[data-testid=\\"property-name\\"], h1, h2")?.textContent')
        logger.info(f"Detected Name: {name}")
        
        # Check if amenities are visible
        amenities_html = page.evaluate('document.querySelector("[data-testid=\\"property-most-popular-facilities-wrapper\\"], .hp_desc_important_facilities")?.innerHTML')
        logger.info(f"Amenities Wrapper Found: {bool(amenities_html)}")
        
        # Take a screenshot to see what's happening
        page.screenshot(path="mobile_debug.png")
        logger.info("Screenshot saved to mobile_debug.png")
        
        browser.close()

if __name__ == "__main__":
    debug_mobile_details()
