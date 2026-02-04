"""
Advanced web scraper using Playwright to bypass anti-bot protection
This scraper uses a stable launch-per-request model for FastAPI compatibility.
"""

from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeout
from typing import List, Dict, Optional
import logging
import time
from datetime import datetime, timedelta

from config import BOOKING_CONFIG, SCRAPER_CONFIG

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class PlaywrightBookingScraper:
    """Advanced scraper using Playwright for Booking.com"""
    
    def __init__(self):
        self.base_url = BOOKING_CONFIG["base_url"]
        self.timeout = SCRAPER_CONFIG["timeout"] * 1000  # Convert to milliseconds
        self.max_retries = SCRAPER_CONFIG["max_retries"]

    @staticmethod
    def setup_route(page):
        """Aggressive resource and script blocking (relaxed for reliability)"""
        def handle_route(route):
            url = route.request.url
            resource_type = route.request.resource_type
            
            # Block heavy/tracking resources
            if resource_type in ["font", "media"]:
                return route.abort()
            
            # Block third-party trackers aggressively
            blocked_domains = ["google-analytics.com", "doubleclick.net", "facebook.net", "adgoogles.com"]
            if any(domain in url for domain in blocked_domains):
                return route.abort()
                
            if resource_type == "image":
                return route.abort()
            
            # Allow all booking-related scripts and AJAX calls
            if "booking.com" in url or "bstatic.com" in url:
                return route.continue_()
            
            # Block other third-party scripts
            if resource_type == "script":
                return route.abort()
            
            return route.continue_()
            
        page.route("**/*", handle_route)

        
    def _build_search_url(self, city: str, checkin: Optional[str] = None, checkout: Optional[str] = None) -> str:
        """Build Booking.com search URL"""
        if not checkin:
            checkin_date = datetime.now() + timedelta(days=BOOKING_CONFIG["default_checkin_offset"])
            checkin = checkin_date.strftime("%Y-%m-%d")
        
        if not checkout:
            checkout_date = datetime.now() + timedelta(days=BOOKING_CONFIG["default_checkout_offset"])
            checkout = checkout_date.strftime("%Y-%m-%d")
        
        params = {
            "ss": city,
            "checkin": checkin,
            "checkout": checkout,
            "group_adults": 2,
            "group_children": 0,
            "no_rooms": 1,
        }
        
        query_string = "&".join([f"{k}={v}" for k, v in params.items()])
        url = f"{self.base_url}/searchresults.html?{query_string}"
        
        logger.info(f"Built search URL: {url}")
        return url
    
    def search_hotels(self, city: str, checkin: Optional[str] = None, checkout: Optional[str] = None) -> List[Dict]:
        """Search hotels using launch-per-request model for threading stability"""
        url = self._build_search_url(city, checkin, checkout)
        
        for attempt in range(self.max_retries):
            try:
                logger.info(f"Playwright search attempt {attempt + 1}/{self.max_retries} for {city}")
                
                with sync_playwright() as p:
                    browser = p.chromium.launch(
                        headless=True,
                        args=['--no-sandbox', '--disable-setuid-sandbox', '--disable-dev-shm-usage', '--disable-blink-features=AutomationControlled']
                    )
                    
                    context = browser.new_context(
                        user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
                        viewport={'width': 1280, 'height': 800},
                        locale='en-US'
                    )
                    
                    try:
                        page = context.new_page()
                        PlaywrightBookingScraper.setup_route(page)
                        
                        logger.info(f"Navigating to search results: {url}")
                        page.goto(url, wait_until='domcontentloaded', timeout=self.timeout)
                        
                        try:
                            page.wait_for_selector('[data-testid="property-card"]', timeout=10000)
                        except: pass
                        
                        # Small delay for content settling
                        time.sleep(1)
                        
                        hotels_data = page.evaluate('''() => {
                            const hotels = [];
                            const cards = document.querySelectorAll('[data-testid="property-card"]');
                            cards.forEach((card, index) => {
                                if (index >= 10) return;
                                try {
                                    const nameElem = card.querySelector('[data-testid="title"]');
                                    const name = nameElem ? nameElem.textContent.trim() : null;
                                    if (!name) return;
                                    
                                    let url = null;
                                    const link = card.querySelector('a[data-testid="title-link"]');
                                    if (link) url = link.href.split('?')[0];
                                    
                                    let price = 0;
                                    const priceElem = card.querySelector('[data-testid="price-and-discounted-price"]');
                                    if (priceElem) {
                                        const m = priceElem.textContent.match(/[\\d,]+/);
                                        if (m) price = parseFloat(m[0].replace(/,/g, ''));
                                    }
                                    
                                    let rating = 0;
                                    const scoreElem = card.querySelector('[data-testid="review-score"]');
                                    if (scoreElem) {
                                        const m = scoreElem.textContent.match(/([\\d.]+)/);
                                        if (m) {
                                            const v = parseFloat(m[1]);
                                            rating = v > 5 ? v / 2 : v;
                                        }
                                    }
                                    
                                    const hotel_id = Math.abs(name.split('').reduce((a, b) => {
                                        a = ((a << 5) - a) + b.charCodeAt(0);
                                        return a & a;
                                    }, 0)) % 100000;
                                    
                                    hotels.push({
                                        hotel_id, name, price, currency: 'INR', 
                                        rating: Math.round(rating * 10) / 10, url 
                                    });
                                } catch (e) {}
                            });
                            return hotels;
                        }''')
                        
                        if hotels_data:
                            logger.info(f"✅ Scraped {len(hotels_data)} hotels")
                            return hotels_data
                    finally:
                        browser.close()
            except Exception as e:
                logger.error(f"Search error on attempt {attempt + 1}: {e}")
                if attempt < self.max_retries - 1:
                    time.sleep(1)
        return []


def fetch_hotels_advanced(city: str, checkin: Optional[str] = None, checkout: Optional[str] = None) -> List[Dict]:
    scraper = PlaywrightBookingScraper()
    return scraper.search_hotels(city, checkin, checkout)


def fetch_hotel_details(hotel_url: str) -> Optional[Dict]:
    """Fetch hotel details with launch-per-request model"""
    try:
        logger.info(f"Fetching hotel details: {hotel_url}")
        with sync_playwright() as p:
            browser = p.chromium.launch(
                headless=True,
                args=['--no-sandbox', '--disable-setuid-sandbox', '--disable-dev-shm-usage', '--disable-blink-features=AutomationControlled']
            )
            
            context = browser.new_context(
                user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                viewport={'width': 1280, 'height': 800},
                locale='en-US',
                timezone_id='Asia/Kolkata',
                permissions=['geolocation']
            )
            
            try:
                page = context.new_page()
                page.add_init_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
                PlaywrightBookingScraper.setup_route(page)

                logger.info(f"Navigating to hotel page...")
                try:
                    # Use domcontentloaded for initial burst, but we'll need to wait for stabilization
                    page.goto(hotel_url, wait_until='domcontentloaded', timeout=30000)
                except Exception as e:
                    logger.warning(f"Initial navigation warning: {e}")
                
                # 1. Handle WAF Challenge
                if page.query_selector('#challenge-container'):
                    logger.info("🛡️ AWS WAF challenge detected. Waiting for resolution...")
                    try:
                        page.wait_for_selector('#challenge-container', state='hidden', timeout=12000)
                        logger.info("✅ Challenge resolved!")
                    except:
                        logger.warning("WAF challenge did not resolve in time.")

                # 2. Stabilization & Interaction
                # High-speed progressive scroll
                page.evaluate("window.scrollTo(0, 800);")
                time.sleep(0.2)
                
                # Scroll to facilities section to load full amenities
                try:
                    page.evaluate("document.querySelector('#hp_facilities_box, [href=\"#hp_facilities_box\"]')?.scrollIntoView();")
                    time.sleep(0.3)
                    # Click "Show all facilities" if it exists
                    show_all = page.query_selector('a[href="#hotelTmpl"], button[data-testid="show-all-facilities"], .show_all_facilities_trigger')
                    if show_all:
                        show_all.click()
                        time.sleep(0.5)
                except: pass
                
                # Scroll to availability for room types
                page.evaluate("document.querySelector('#availability_target')?.scrollIntoView();")
                time.sleep(0.4) # Brief wait for rooms
                
                # Trigger Reviews only if really needed (already getting many from DOM)
                try:
                    review_count = page.evaluate("document.querySelectorAll('[data-testid=\"review-card\"], .review_item').length")
                    if review_count < 3:
                        trigger = page.query_selector('#reviews-tab-trigger, [data-testid="read-all-actionable"]')
                        if trigger:
                            trigger.click()
                            time.sleep(0.8)
                except: pass

                # Final wait for core content
                try:
                    page.wait_for_selector('[data-testid="property-name"]', timeout=3000)
                except: pass

                # --- Extraction Logic ---
                hotel_data = page.evaluate('''() => {
                    const d = {
                        name: '', rating: 0, address: '', description: '',
                        amenities: [], reviews: [], photos: [], room_types: []
                    };
                    
                    // 1. Basic Info (JSON-LD)
                    try {
                        const ld = JSON.parse(document.querySelector('script[type="application/ld+json"]')?.innerText || '{}');
                        d.name = ld.name || '';
                        d.rating = ld.aggregateRating?.ratingValue || 0;
                        d.address = ld.address?.streetAddress || '';
                        d.description = ld.description || '';
                    } catch(e) {}

                    // 2. DOM Fallbacks for basic info
                    if (!d.name) d.name = document.querySelector('[data-testid="property-name"], h2.hp__hotel-name')?.innerText?.trim() || '';
                    if (!d.address) d.address = document.querySelector('.hp_address_subtitle, [data-testid="address_badge"]')?.innerText?.trim() || '';
                    if (!d.description) {
                        const descEl = document.querySelector('#property_description_content, [data-testid="property-description"]');
                        d.description = descEl ? descEl.innerText.trim() : '';
                    }

                    // 3. Amenities (Full extraction without limits)
                    const seenAms = new Set();
                    
                    // First, popular facilities
                    document.querySelectorAll('.hp_desc_important_facilities div, [data-testid="property-most-popular-facilities-wrapper"] span, .important_facility').forEach(el => {
                        const text = el.innerText.trim();
                        if (text && !seenAms.has(text)) {
                            seenAms.add(text);
                            d.amenities.push({ category: 'Popular', name: text });
                        }
                    });

                    // Next, full facilities list by category
                    document.querySelectorAll('.hotel_facilities_block, .hp-facilities-box, #hp_facilities_box .hotel_facilities_block').forEach(block => {
                        const category = block.querySelector('h3, h4')?.innerText?.trim() || 'General';
                        block.querySelectorAll('li, .hp-facilites-list li').forEach(item => {
                            const text = item.innerText.trim();
                            if (text && !seenAms.has(text)) {
                                seenAms.add(text);
                                d.amenities.push({ category: category, name: text });
                            }
                        });
                    });

                    // Catch-all for any other lists in the facilities area
                    document.querySelectorAll('#hp_facilities_box li, [data-testid="property-section-content"] li').forEach(el => {
                        const text = el.innerText.trim();
                        if (text && !seenAms.has(text)) {
                            seenAms.add(text);
                            d.amenities.push({ category: 'General', name: text });
                        }
                    });

                    // 4. Reviews extraction (Aligned with HotelReview model)
                    const reviewSelectors = [
                        '[data-testid="review-card"]',
                        '.review_item',
                        '.c-review-block',
                        '[data-testid="featuredreview"]'
                    ];
                    
                    const seenReviews = new Set();
                    for (const sel of reviewSelectors) {
                        document.querySelectorAll(sel).forEach(el => {
                            const text = el.querySelector('[data-testid="review-text"], .review_item_main_content, .c-review__body, [data-testid="featuredreview-text"]')?.innerText?.trim();
                            if (text && !seenReviews.has(text) && seenReviews.size < 5) {
                                seenReviews.add(text);
                                // Enhanced Author Extraction
                                const authorSelectors = [
                                    '.review_item_reviewer h4',
                                    '[data-testid="review-author-name"]',
                                    '.bui-avatar-block__title',
                                    '[data-testid="featuredreview-avatar"]',
                                    '.review-card__header__name'
                                ];
                                let author = 'Guest';
                                for (const aSel of authorSelectors) {
                                    const aEl = el.querySelector(aSel);
                                    if (aEl && aEl.innerText.trim()) {
                                        author = aEl.innerText.trim().split('\\n')[0]; // Take first line (name)
                                        break;
                                    }
                                }
                                
                                // Enhanced Score Extraction
                                let scoreEl = el.querySelector('[data-testid="review-score-badge"], [data-testid="review-scoreBadge"], .bui-review-score__badge, .review-score-badge, .a3b87295b3, .ebf0170a44, .d1921f0084');
                                let score = 0;
                                if (scoreEl) {
                                    let scoreText = scoreEl.innerText || scoreEl.getAttribute('aria-label') || '0';
                                    score = parseFloat(scoreText.match(/[\\d.]+/)?.[0] || '0');
                                } else {
                                    // Fallback to searching any div/span within the card that has a numeric class or content
                                    const scoreCandidates = Array.from(el.querySelectorAll('div, span')).filter(e => /^\\d+(\\.\\d+)?$/.test(e.innerText.trim()));
                                    if (scoreCandidates.length > 0) {
                                        score = parseFloat(scoreCandidates[0].innerText);
                                    }
                                }
                                
                                // Final fallback for snippet reviews (featured) which often don't have individual scores visible
                                if (score === 0 && d.rating > 0) score = d.rating;
                                
                                d.reviews.push({ reviewer_name: author, comment: text, rating: score });

                            }
                        });
                        if (d.reviews.length >= 3) break;
                    }

                    // 5. Photos extraction (Skipped as requested)
                    d.photos = [];

                    // 6. Room Types extraction (Aligned with RoomType model)
                    const roomNames = new Set();
                    const roomSelectors = [
                        '.rt-room-info',
                        '[data-testid="room-title"]',
                        '.hprt-roomtype-link',
                        '[data-room-id] .hprt-roomtype-icon-link',
                        '.hp-rt-room-name',
                        '[data-testid="rt-room-card"] .hprt-roomtype-link',
                        '.hprt-table-cell-roomtype .hprt-roomtype-icon-link',
                        '.room-info a'
                    ];
                    for (const rs of roomSelectors) {
                        document.querySelectorAll(rs).forEach(el => {
                            const name = el.innerText.trim().split('\\n')[0];
                            if (name && name.length > 3 && !roomNames.has(name) && roomNames.size < 10) {
                                roomNames.add(name);
                                d.room_types.push({ name: name, price: 0.0, currency: 'INR' });
                            }
                        });
                    }

                    // Secondary fallback for room types from window data if extraction failed
                    if (d.room_types.length === 0) {
                        try {
                            const b_env = window.booking?.env || {};
                            const rooms = b_env.b_room_group || b_env.hprt_room_data || [];
                            rooms.forEach(r => {
                                if (r.name && !roomNames.has(r.name)) {
                                    roomNames.add(r.name);
                                    d.room_types.push({ name: r.name, price: 0.0, currency: 'INR' });
                                }
                            });
                        } catch(e) {}
                    }

                    
                    return d;
                }''')
                
                # Post-process in python
                if hotel_data and hotel_data.get('name'):
                    name = hotel_data['name']
                    # Use absolute value of hash to avoid negative IDs
                    hotel_id = abs(hash(name)) % 100000
                    hotel_data['hotel_id'] = hotel_id
                    
                    # Fix rating if exceeds 5 (Booking uses 10-point scale sometimes)
                    if hotel_data.get('rating') and hotel_data['rating'] > 5:
                        hotel_data['rating'] = round(hotel_data['rating'] / 2, 1)
                    
                    logger.info(f"✅ Successfully fetched details for: {name}")
                    return hotel_data
                
                return None
            finally:
                browser.close()
    except Exception as e:
        logger.error(f"Detail error for {hotel_url}: {e}")
        return None

