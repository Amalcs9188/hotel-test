from playwright.sync_api import sync_playwright
import json

def debug_hotel():
    url = "https://www.booking.com/hotel/in/the-taj-mahal-palace-mumbai.html"
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'
        )
        page = context.new_page()
        print(f"Navigating to {url}...")
        page.goto(url, wait_until='domcontentloaded')
        
        # Take screenshot
        page.screenshot(path="debug_hotel.png")
        print("Screenshot saved to debug_hotel.png")
        
        # Check for name
        name = page.evaluate('() => document.querySelector("[data-testid=\\"property-name\\"], h1, h2")?.textContent')
        print(f"Extracted Name: {name}")
        
        # Check for JSON-LD
        json_ld = page.evaluate('() => Array.from(document.querySelectorAll("script[type=\\"application/ld+json\\"]")).map(s => s.textContent.substring(0, 100))')
        print(f"JSON-LD Count: {len(json_ld)}")
        print(f"JSON-LD Samples: {json_ld}")
        
        # Dump some HTML
        html = page.content()
        with open("debug_hotel.html", "w", encoding="utf-8") as f:
            f.write(html)
        print("HTML saved to debug_hotel.html")
        
        browser.close()

if __name__ == "__main__":
    debug_hotel()
