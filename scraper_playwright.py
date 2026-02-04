"""
Advanced web scraper using Playwright to bypass anti-bot protection
This scraper can successfully fetch real hotel data from Booking.com
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
        """
        Search for hotels using Playwright (bypasses anti-bot protection)
        
        Args:
            city: City name to search
            checkin: Check-in date (YYYY-MM-DD format)
            checkout: Check-out date (YYYY-MM-DD format)
            
        Returns:
            List of hotel dictionaries
        """
        url = self._build_search_url(city, checkin, checkout)
        
        for attempt in range(self.max_retries):
            try:
                logger.info(f"Playwright attempt {attempt + 1}/{self.max_retries} for {city}")
                
                with sync_playwright() as p:
                    # Launch browser with stealth settings
                    browser = p.chromium.launch(
                        headless=True,
                        args=[
                            '--no-sandbox',
                            '--disable-setuid-sandbox',
                            '--disable-dev-shm-usage',
                            '--disable-blink-features=AutomationControlled'
                        ]
                    )
                    
                    # Create context with realistic settings
                    context = browser.new_context(
                        viewport={'width': 1920, 'height': 1080},
                        user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                        locale='en-US',
                        timezone_id='America/New_York'
                    )
                    
                    logger.info(f"Navigating to: {url}")
                    
                    # Performance optimization: Block light resources (fonts, media)
                    # Keeping images and stylesheets for reliable heart/card rendering
                    page.route("**/*", lambda route: route.abort() if route.request.resource_type in ["font", "media"] else route.continue_())
                    
                    page.goto(url, wait_until='domcontentloaded', timeout=self.timeout)
                    
                    # Wait for hotel cards to load
                    try:
                        page.wait_for_selector('[data-testid="property-card"]', timeout=15000)
                        logger.info("Hotel cards loaded successfully!")
                    except PlaywrightTimeout:
                        logger.warning("Timeout waiting for hotel cards, trying alternative selector")
                        # Try alternative selectors
                        page.wait_for_selector('.sr_item', timeout=10000)
                    
                    # Small delay to ensure content is fully loaded
                    time.sleep(2)
                    
                    # Extract hotel data using JavaScript
                    hotels_data = page.evaluate('''() => {
                        const hotels = [];
                        const cards = document.querySelectorAll('[data-testid="property-card"]');
                        
                        cards.forEach((card, index) => {
                            if (index >= 10) return; // Limit to 10 hotels
                            
                            try {
                                // Extract hotel name
                                const nameElem = card.querySelector('[data-testid="title"]');
                                const name = nameElem ? nameElem.textContent.trim() : null;
                                
                                if (!name) return;
                                
                                // Extract hotel URL - try multiple selectors
                                let url = null;
                                const linkSelectors = [
                                    'a[data-testid="title-link"]',
                                    'a[href*="/hotel/"]',
                                    'a.e13098a59f',
                                    'h3 a',
                                    'a[aria-label]'
                                ];
                                
                                for (const selector of linkSelectors) {
                                    const linkElem = card.querySelector(selector);
                                    if (linkElem) {
                                        const href = linkElem.getAttribute('href');
                                        if (href && href.includes('/hotel/')) {
                                            // Convert relative URL to absolute
                                            url = href.startsWith('http') ? href : 'https://www.booking.com' + href;
                                            // Remove query parameters for cleaner URL
                                            url = url.split('?')[0];
                                            break;
                                        }
                                    }
                                }
                                
                                // Extract price
                                let price = 0;
                                const priceSelectors = [
                                    '[data-testid="price-and-discounted-price"]',
                                    '.prco-valign-middle-helper',
                                    '.bui-price-display__value',
                                    '[data-testid="price-for-x-nights"]'
                                ];
                                
                                for (const selector of priceSelectors) {
                                    const priceElem = card.querySelector(selector);
                                    if (priceElem) {
                                        const priceText = priceElem.textContent;
                                        const priceMatch = priceText.match(/[\d,]+/);
                                        if (priceMatch) {
                                            price = parseFloat(priceMatch[0].replace(/,/g, ''));
                                            break;
                                        }
                                    }
                                }
                                
                                // Extract rating - try multiple selectors
                                let rating = 0;
                                const ratingSelectors = [
                                    '[data-testid="review-score"]',
                                    '.b5cd09854e',
                                    '[aria-label*="Scored"]',
                                    '.bui-review-score__badge'
                                ];
                                
                                for (const selector of ratingSelectors) {
                                    const ratingElem = card.querySelector(selector);
                                    if (ratingElem) {
                                        // Try to find the numeric rating
                                        const ratingDiv = ratingElem.querySelector('div[aria-label]') || ratingElem;
                                        const ariaLabel = ratingDiv.getAttribute('aria-label');
                                        
                                        if (ariaLabel) {
                                            const ratingMatch = ariaLabel.match(/([\d.]+)/);
                                            if (ratingMatch) {
                                                const ratingValue = parseFloat(ratingMatch[1]);
                                                // Convert from 10-scale to 5-scale if needed
                                                rating = ratingValue > 5 ? ratingValue / 2 : ratingValue;
                                                break;
                                            }
                                        }
                                        
                                        // Try direct text content
                                        const ratingText = ratingElem.textContent;
                                        const textMatch = ratingText.match(/([\d.]+)/);
                                        if (textMatch) {
                                            const ratingValue = parseFloat(textMatch[1]);
                                            rating = ratingValue > 5 ? ratingValue / 2 : ratingValue;
                                            break;
                                        }
                                    }
                                }
                                
                                // Generate hotel ID from name
                                const hotel_id = Math.abs(name.split('').reduce((a, b) => {
                                    a = ((a << 5) - a) + b.charCodeAt(0);
                                    return a & a;
                                }, 0)) % 100000;
                                
                                hotels.push({
                                    hotel_id: hotel_id,
                                    name: name,
                                    price: price,
                                    currency: 'INR',
                                    rating: Math.round(rating * 10) / 10,
                                    url: url
                                });
                            } catch (e) {
                                console.log('Error parsing hotel card:', e);
                            }
                        });
                        
                        return hotels;
                    }''')
                    
                    browser.close()
                    
                    if hotels_data and len(hotels_data) > 0:
                        logger.info(f"✅ Successfully scraped {len(hotels_data)} hotels for {city}")
                        return hotels_data
                    else:
                        logger.warning(f"No hotels found for {city}")
                        return []
                
            except PlaywrightTimeout as e:
                logger.error(f"Playwright timeout on attempt {attempt + 1}: {e}")
                if attempt < self.max_retries - 1:
                    time.sleep(SCRAPER_CONFIG["retry_delay"] * (attempt + 1))
                else:
                    logger.error(f"Failed after {self.max_retries} attempts")
                    return []
                    
            except Exception as e:
                logger.error(f"Unexpected error on attempt {attempt + 1}: {e}")
                if attempt < self.max_retries - 1:
                    time.sleep(SCRAPER_CONFIG["retry_delay"] * (attempt + 1))
                else:
                    logger.error(f"Failed after {self.max_retries} attempts")
                    return []
        
        return []


# Update the main fetch function to use Playwright
def fetch_hotels_advanced(city: str, checkin: Optional[str] = None, checkout: Optional[str] = None) -> List[Dict]:
    """
    Fetch hotels using advanced Playwright scraper
    
    Args:
        city: City name to search
        checkin: Check-in date (YYYY-MM-DD format)
        checkout: Check-out date (YYYY-MM-DD format)
        
    Returns:
        List of hotel dictionaries
    """
    scraper = PlaywrightBookingScraper()
    return scraper.search_hotels(city, checkin, checkout)


def fetch_hotel_details(hotel_url: str) -> Optional[Dict]:
    """
    Fetch detailed information about a specific hotel
    
    Args:
        hotel_url: Full Booking.com hotel URL
        
    Returns:
        Dictionary with comprehensive hotel details
    """
    try:
        logger.info(f"Fetching hotel details from: {hotel_url}")
        with sync_playwright() as p:
            # Launch browser with slightly more stealth
            browser = p.chromium.launch(
                headless=True,
                args=['--disable-blink-features=AutomationControlled']
            )
            context = browser.new_context(
                viewport={'width': 1920, 'height': 1080},
                user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
                locale='en-US'
            )
            page = context.new_page()
            
            # Performance optimization: Block light resources (fonts, media)
            # Keeping images and stylesheets as they are often needed for correct DOM rendering/scripts
            page.route("**/*", lambda route: route.abort() if route.request.resource_type in ["font", "media"] else route.continue_())
            
            # Restore headers for better compatibility
            page.set_extra_http_headers({
                'Accept-Language': 'en-US,en;q=0.9',
                'Referer': 'https://www.google.com/'
            })
            
            # Pipe console logs
            page.on('console', lambda msg: logger.info(f"BROWSER: {msg.text}"))
            
            # Navigate to hotel page
            # Navigate to hotel page
            logger.info(f"Navigating to hotel page...")
            page.goto(hotel_url, wait_until='domcontentloaded', timeout=60000)
            
            # --- FAST-EXIT STRATEGY ---
            # Attempt immediate extraction from JSON-LD/Initial DOM
            try:
                fast_data = page.evaluate('''() => {
                    const d = { name: '', rating: 0, reviews: [], amenities: [] };
                    
                    // JSON-LD
                    const scripts = document.querySelectorAll('script[type="application/ld+json"]');
                    scripts.forEach(s => {
                        try {
                            const data = JSON.parse(s.textContent);
                            if (data['@type'] === 'Hotel' || data['@type'] === 'Accommodation') {
                                d.name = data.name;
                                if (data.aggregateRating) d.rating = parseFloat(data.aggregateRating.ratingValue);
                                if (data.review) d.reviews = Array.isArray(data.review) ? data.review : [data.review];
                                if (data.amenityFeature) d.amenities = data.amenityFeature;
                            }
                        } catch(e){}
                    });
                    
                    // Basic DOM Name
                    if (!d.name) {
                        const h = document.querySelector('h2.pp-header__title, #hp_hotel_name');
                        if (h) d.name = h.textContent.trim();
                    }
                    
                    return d;
                }''')
                
                # STRICT FAST-EXIT: Only skip scroll if we have Name, 3+ Reviews, AND 5+ Amenities
                if fast_data['name'] and len(fast_data['reviews']) >= 3 and len(fast_data['amenities']) >= 5:
                    logger.info(f"🚀 Fast-Exit: Found {len(fast_data['reviews'])} reviews and {len(fast_data['amenities'])} amenities!")
                    # We still need to run the full extraction to standardize the format,
                    # but we can skip the scrolling delays.
                    pass # Continue to extraction, but skip scrolling
                else:
                    logger.info("Fast-Exit insufficient, proceeding to robust load...")
                    
                    # Wait for core content to render since we only waited for domcontentloaded
                    try:
                        page.wait_for_selector('h1, h2, [data-testid="property-name"]', timeout=10000)
                    except:
                        logger.warning("Fallback: Core content timeout")
                    
                    # Scroll only if fast-exit didn't find enough
                    for i in range(1, 4):
                        page.evaluate(f"window.scrollTo(0, {i * 1500})")
                        time.sleep(1.0)
                    # Helper: Scroll to bottom once to ensure footer triggers
                    page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
                    time.sleep(1.0)
            except Exception as e:
                logger.warning(f"Fast-Exit check failed: {e}")
            
            # --- END FAST-EXIT ---
            
            # If no review cards visible, try to click the reviews button/tab to load them
            try:
                # Specific wait for reviews if we are in fallback mode
                if not page.query_selector('[data-testid="review-card"]'):
                     page.wait_for_selector('[data-testid="review-card"]', timeout=5000)
            except: pass

            try:
                if not page.query_selector('[data-testid="review-card"], .review_item, .c-review-block'):
                    # Try multiple triggers
                    for selector in ['[data-testid="read-all-actionable"]', '[data-testid="review-score-read-all"]', '.hp_reviews_count', '#show_reviews_tab', 'text="Read all reviews"']:
                        review_trigger = page.query_selector(selector)
                        if review_trigger:
                            logger.info(f"Attempting to load reviews via click on {selector}...")
                            review_trigger.scroll_into_view_if_needed()
                            review_trigger.click(force=True)
                            # Wait for reviews to load in modal or new section
                            # Wait for reviews to load in modal or new section
                            page.wait_for_selector('[data-testid="review-card"], .review_item, .c-review-block, [data-testid="review-author-name"]', timeout=10000)
                            logger.info("Reviews UI should be visible now.")
                            time.sleep(1.5)
                            break
            except Exception as e:
                logger.debug(f"Click reviews failed: {e}")

            
            # Extract all hotel details using JavaScript with JSON-LD support
            hotel_data = page.evaluate('''() => {
                const details = {
                    name: '',
                    rating: 0,
                    address: '',
                    description: '',
                    amenities: [],
                    reviews: [],
                    photos: [],
                    room_types: [],
                    check_in_time: '',
                    check_out_time: '',
                    policies: '',
                    contact_phone: '',
                    contact_email: ''
                };
                
                // Try to extract data from JSON-LD first
                const jsonLdElems = document.querySelectorAll('script[type="application/ld+json"]');
                jsonLdElems.forEach(el => {
                    try {
                        const data = JSON.parse(el.textContent);
                        if (data['@type'] === 'Hotel' || data['@type'] === 'Accommodation' || data['@type'] === 'LodgingBusiness') {
                            if (data.name) details.name = data.name;
                            if (data.description) details.description = data.description;
                            if (data.address) {
                                if (typeof data.address === 'string') {
                                    details.address = data.address;
                                } else {
                                    details.address = [
                                        data.address.streetAddress,
                                        data.address.addressLocality,
                                        data.address.addressRegion,
                                        data.address.postalCode,
                                        data.address.addressCountry
                                    ].filter(Boolean).join(', ');
                                }
                            }
                            if (data.amenityFeature) {
                                details.amenities = [];
                                const amenities = Array.isArray(data.amenityFeature) ? data.amenityFeature : [data.amenityFeature];
                                amenities.forEach(am => {
                                   if (typeof am === 'object' && am.name) details.amenities.push({ category: 'General', name: am.name });
                                   else if (typeof am === 'string') details.amenities.push({ category: 'General', name: am });
                                });
                            }
                            if (data.image) {
                                const images = Array.isArray(data.image) ? data.image : [data.image];
                                images.forEach(img => {
                                    const url = typeof img === 'string' ? img : img.url;
                                    if (url) details.photos.push({ url });
                                });
                            }
                            if (data.aggregateRating) {
                                details.rating = data.aggregateRating.ratingValue / 2; // Convert to 5-star scale
                            }
                            // Only use JSON-LD reviews as a fallback if DOM is empty later
                            if (data.review) {
                                details._jsonld_reviews = Array.isArray(data.review) ? data.review : [data.review];
                            }
                        }
                    } catch (e) {}
                });
                
                // Fallback and refine with DOM selectors
                if (!details.name) {
                    const nameSelectors = [
                        'h2[data-testid="property-name"]',
                        '.pp-header__title',
                        'h1',
                        'h2',
                        '.hp__hotel-name',
                        '#hp_hotel_name',
                        '[data-testid="title"]'
                    ];
                    for (const selector of nameSelectors) {
                        const el = document.querySelector(selector);
                        if (el) {
                            details.name = el.textContent.trim().replace(/\\n/g, ' ');
                            break;
                        }
                    }
                }
                
                // If still no name, use title
                if (!details.name) details.name = document.title.split('-')[0].split('|')[0].trim();

                
                // Extract rating - try multiple selectors
                const ratingSelectors = [
                    '[data-testid="review-score-component"]',
                    '.b5cd09854e',
                    '[aria-label*="Scored"]',
                    '.review-score-badge',
                    '.bui-review-score__badge',
                    '[data-testid="review-score"]'
                ];
                
                for (const selector of ratingSelectors) {
                    const el = document.querySelector(selector);
                    if (el) {
                        const text = el.textContent;
                        const match = text.match(/([\\d.]+)/);
                        if (match) {
                            const val = parseFloat(match[1]);
                            details.rating = val > 5 ? val / 2 : val;
                            break;
                        }
                    }
                }
                
                // Extract address
                const addressSelectors = [
                    '[data-testid="address"]',
                    '.hp_address_subtitle',
                    '[data-node_tt_id="location_score_tooltip"]',
                    '.pp-header__address',
                    '.address'
                ];
                
                for (const selector of addressSelectors) {
                    const el = document.querySelector(selector);
                    if (el) {
                        details.address = el.textContent.trim();
                        break;
                    }
                }
                
                // Extract description
                const descSelectors = [
                    '[data-testid="property-description"]',
                    '#property_description_content',
                    '.hp-description',
                    '.property_description_content'
                ];
                
                for (const selector of descSelectors) {
                    const el = document.querySelector(selector);
                    if (el) {
                        details.description = el.textContent.trim();
                        break;
                    }
                }
                
                // Extract amenities
                const amenityGroups = document.querySelectorAll('[data-testid="facility-group"], [data-testid="facility-group-container"], .hp-facility-block, .facilitiesChecklistSection, .b43e553776');
                amenityGroups.forEach(group => {
                    const titleEl = group.querySelector('[data-testid="facility-group-title"], .bui-title__text, h3, .e7addce19e');
                    const category = titleEl ? titleEl.textContent.trim() : 'General';
                    
                    const items = group.querySelectorAll('li, [data-testid="facility-item"], .bui-list__item, [data-testid="facility-group-item"]');
                    items.forEach(item => {
                        const name = item.textContent.trim();
                        if (name) {
                            details.amenities.push({ category, name });
                        }
                    });
                });
                
                // Fallback for amenities if empty
                if (details.amenities.length === 0) {
                    document.querySelectorAll('.important_facility, .hp_facility_list li, .facility-item').forEach(el => {
                        details.amenities.push({ category: 'Popular', name: el.textContent.trim() });
                    });
                }
                
                // 5. Reviews extraction (DOM)
                if (details.reviews.length === 0) {
                    const reviewSelectors = [
                        '[data-testid="review-card"]',
                        '.review_item',
                        '.c-review-block',
                        '.featured_review',
                        '.review_list_new_item_block',
                        '[data-testid="review-author-name"]'
                    ];
                    
                    let reviewCards = [];
                    for (const s of reviewSelectors) {
                        const found = document.querySelectorAll(s);
                        console.log(`Selector ${s} found ${found.length} elements`);
                        if (found.length > 0) { 
                            if (s === '[data-testid="review-author-name"]') {
                                reviewCards = Array.from(found).map(el => el.closest('div, li') || el);
                            } else {
                                reviewCards = Array.from(found); 
                            }
                            break; 
                        }
                    }
                    
                    reviewCards.forEach((card, idx) => {
                        if (idx >= 10) return;
                        
                        const cardText = card.innerText || '';
                        
                        // Author - try multiple common selectors
                        let reviewer = 'Anonymous';
                        const authorSelectors = [
                            '[data-testid="review-author-name"]',
                            '.bui-avatar-block__title',
                            '.c-review-block__title',
                            '.review_item_reviewer_name',
                            '.bui-avatar-block__text',
                            '.a3332d4613', 
                            '.be659bb4c2 [class*="title"]',
                            '.be659bb4c2 div:first-child',
                            '.review-card__author',
                            '.review-author-name'
                        ];
                        for (const s of authorSelectors) {
                            const el = card.querySelector(s);
                            if (el && el.textContent.trim()) {
                                reviewer = el.textContent.trim();
                                break;
                            }
                        }
                        // Fallback: If still anonymous, take first line if it looks like a name (short)
                        if (reviewer === 'Anonymous' && cardText) {
                            const firstLine = cardText.split('\\n')[0].trim();
                            if (firstLine && firstLine.length > 0 && firstLine.length < 40) reviewer = firstLine;
                        }
                        
                        // Rating - look for badges or text patterns
                        let rating = 0;
                        const scoreSelectors = [
                            '[data-testid="review-score-badge"]',
                            '.bui-review-score__badge',
                            '.review-score-badge',
                            '.b5cd09854e',
                            '.abf0933828',
                            '.a7da303032',
                            '.d22a77730d',
                            '.be06d33c8b',
                            '[aria-label*="Scored"]'
                        ];
                        for (const s of scoreSelectors) {
                            const scoreEl = card.querySelector(s);
                            if (scoreEl) {
                                const scoreTxt = scoreEl.getAttribute('aria-label') || scoreEl.textContent;
                                const m = scoreTxt.match(/([\\d.]+)/);
                                if (m) {
                                    rating = parseFloat(m[1]);
                                    break;
                                }
                            }
                        }
                        // Fallback: search for X/10 or single number at start/end of a line
                        if (rating === 0) {
                            const m1 = cardText.match(/(\d+\.?\d*)\/10/);
                            if (m1) rating = parseFloat(m1[1]);
                            else {
                                const m2 = cardText.match(/(?:^|\\n)\s*(\d+\.?\d*)\s*(?:\\n|$)/);
                                if (m2) rating = parseFloat(m2[1]);
                            }
                        }
                        
                        // Comment
                        const title = card.querySelector('[data-testid="review-title"], .review_item_header_content, .c-review-block__title')?.textContent.trim() || '';
                        const pos = card.querySelector('[data-testid="review-positive-text"], .c-review__body--translated, .c-review__body')?.textContent.trim() || '';
                        const neg = card.querySelector('[data-testid="review-negative-text"]')?.textContent.trim() || '';
                        
                        let comment = [title, pos, neg].filter(Boolean).join('. ').trim();
                        if (!comment && cardText) {
                            comment = cardText.replace(/\\n/g, ' ').substring(0, 300).trim();
                        }
                        
                        const dateEl = card.querySelector('[data-testid="review-date"], .c-review-block__date, .review_item_date');
                        const date = dateEl ? dateEl.textContent.trim() : '';
                        
                        if (comment || reviewer !== 'Anonymous') {
                            details.reviews.push({ 
                                reviewer_name: reviewer, 
                                rating: rating > 10 ? rating / 10 : rating, 
                                comment, 
                                date 
                            });
                        }
                    });
                }

                // 6. Photos
                const photoSelectors = [
                    '[data-testid="gallery-image"] img',
                    '.hp-gallery-image img',
                    '.hotel_main_gallery img',
                    '[data-testid="hotel-gallery"] img',
                    '.bh-photo-grid-item img',
                    '.bh-photo-grid-thumb img',
                    '.gallery-side-reviews-wrapper img'
                ];
                for (const s of photoSelectors) {
                    const imgs = document.querySelectorAll(s);
                    console.log(`Selector ${s} found ${imgs.length} images`);
                    if (imgs.length > 0) {
                        imgs.forEach((img, i) => {
                            if (i < 20) {
                                const url = img.src || img.getAttribute('src') || img.getAttribute('data-lazy') || img.getAttribute('data-src');
                                if (url && !url.includes('placeholder')) details.photos.push({ url, caption: img.alt || '' });
                            }
                        });
                        break;
                    }
                }
                
                // 7. Room Types
                const roomSelectors = ['[data-testid="room-card"]', '.hprt-table tr', '.hp-room-details'];
                for (const s of roomSelectors) {
                    const cards = document.querySelectorAll(s);
                    if (cards.length > 0) {
                        cards.forEach(card => {
                            const nameEl = card.querySelector('.hprt-roomtype-icon-link, [data-testid="room-name"], .room-name');
                            const priceEl = card.querySelector('.bui-price-display__value, .prco-valign-middle-helper, [data-testid="price-and-discounted-price"]');
                            if (nameEl && priceEl) {
                                details.room_types.push({
                                    name: nameEl.textContent.trim(),
                                    price: parseFloat(priceEl.textContent.replace(/[^\\d.]/g, '')),
                                    currency: 'INR'
                                });
                            }
                        });
                        break;
                    }
                }
                
                
                // Fallback for reviews if DOM was empty
                if (details.reviews.length === 0 && details._jsonld_reviews && details._jsonld_reviews.length > 0) {
                    details._jsonld_reviews.forEach(rev => {
                        if (details.reviews.length < 10) {
                            details.reviews.push({
                                reviewer_name: rev.author?.name || rev.author || 'Anonymous',
                                rating: (rev.reviewRating?.ratingValue || 0) / 2,
                                comment: rev.reviewBody || rev.description || '',
                                date: rev.datePublished || rev.dateCreated || ''
                            });
                        }
                    });
                }
                
                return details;
            }''')
            
            browser.close()
            
            if hotel_data and hotel_data.get('name'):
                # Generate hotel ID from name in Python
                name = hotel_data['name']
                hotel_id = 0
                for char in name:
                    hotel_id = ((hotel_id << 5) - hotel_id) + ord(char)
                    hotel_id &= 0xFFFFFFFF # Keep it as 32-bit int
                
                hotel_data['hotel_id'] = abs(hotel_id) % 100000
                logger.info(f"✅ Successfully fetched details for: {hotel_data['name']}")
                return hotel_data
            else:
                logger.warning("Could not extract hotel details - mandatory field 'name' not found")
                return None
                
    except Exception as e:
        logger.error(f"Error fetching hotel details: {e}")
        return None

