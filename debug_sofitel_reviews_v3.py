
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
    try:
        page.goto(url, wait_until='domcontentloaded', timeout=30000)
    except:
        print("Timeout on goto, continuing...")
    
    # Wait for core content
    time.sleep(3)
    
    # Scroll to trigger loads
    print("Scrolling...")
    page.evaluate("window.scrollTo(0, 1500)")
    time.sleep(2)
    
    page.screenshot(path="sofitel_debug.png")
    print("Screenshot saved to sofitel_debug.png")

    # Search for the specific text and capture surrounding HTML
    capture = page.evaluate('''() => {
        const searchText = "Sofitel has a beautiful and fragrant atmosphere";
        const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT, null, false);
        let node;
        while(node = walker.nextNode()) {
            if (node.textContent.includes(searchText)) {
                let parent = node.parentElement;
                // Go up enough levels to see the container
                let container = parent;
                for(let i=0; i<10; i++) {
                    if (container && container.parentElement) container = container.parentElement;
                }
                return {
                    found: true,
                    html: container ? container.outerHTML : "CONTAINER NOT FOUND",
                    text: node.textContent.trim()
                };
            }
        }
        return { found: false, body_peek: document.body.innerText.substring(0, 500) };
    }''')
    
    import json
    with open("review_context_v3.json", "w", encoding="utf-8") as f:
        json.dump(capture, f, indent=2)
    
    print(f"Capture results saved to review_context_v3.json. Found: {capture['found']}")
    browser.close()
