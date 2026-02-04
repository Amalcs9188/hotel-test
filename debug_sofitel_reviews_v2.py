
from playwright.sync_api import sync_playwright
import time

url = "https://www.booking.com/hotel/in/sofitel-mumbai-bkc.html"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(
        user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        viewport={'width': 1280, 'height': 2000}
    )
    
    print(f"Navigating to {url}...")
    page.goto(url, wait_until='networkidle')
    
    # Scroll slowly to ensure all potential reviews load
    for i in range(1, 4):
        page.evaluate(f"window.scrollTo(0, {i * 1000})")
        time.sleep(1)

    # Search for the specific text and capture surrounding HTML
    capture = page.evaluate('''() => {
        const searchText = "Sofitel has a beautiful and fragrant atmosphere";
        const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT, null, false);
        let node;
        while(node = walker.nextNode()) {
            if (node.textContent.includes(searchText)) {
                // Return parent HTML for inspection
                let parent = node.parentElement;
                // Go up a few levels to get the card
                for(let i=0; i<5; i++) {
                    if (parent && parent.parentElement) parent = parent.parentElement;
                }
                return {
                    found: true,
                    html: parent ? parent.outerHTML : "PARENT NOT FOUND",
                    text: node.textContent.trim()
                };
            }
        }
        return { found: false, html: document.body.innerHTML.substring(0, 10000) };
    }''')
    
    import json
    with open("review_context.json", "w", encoding="utf-8") as f:
        json.dump(capture, f, indent=2)
    
    print(f"Capture results saved to review_context.json. Found: {capture['found']}")
    browser.close()
