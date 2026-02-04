"""
Web scraper module for fetching real hotel data from Booking.com
"""

import requests
from bs4 import BeautifulSoup
from typing import List, Dict, Optional
import time
import random
from datetime import datetime, timedelta
from fake_useragent import UserAgent
import logging

from config import SCRAPER_CONFIG, BOOKING_CONFIG

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class BookingComScraper:
    """Scraper for Booking.com hotel data"""
    
    def __init__(self):
        self.base_url = BOOKING_CONFIG["base_url"]
        self.timeout = SCRAPER_CONFIG["timeout"]
        self.max_retries = SCRAPER_CONFIG["max_retries"]
        self.retry_delay = SCRAPER_CONFIG["retry_delay"]
        self.ua = UserAgent()
        
    def _get_headers(self) -> Dict[str, str]:
        """Generate request headers with random user agent"""
        return {
            "User-Agent": self.ua.random,
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1"
        }
    
    def _build_search_url(self, city: str, checkin: Optional[str] = None, checkout: Optional[str] = None) -> str:
        """Build Booking.com search URL"""
        # Calculate default dates if not provided
        if not checkin:
            checkin_date = datetime.now() + timedelta(days=BOOKING_CONFIG["default_checkin_offset"])
            checkin = checkin_date.strftime("%Y-%m-%d")
        
        if not checkout:
            checkout_date = datetime.now() + timedelta(days=BOOKING_CONFIG["default_checkout_offset"])
            checkout = checkout_date.strftime("%Y-%m-%d")
        
        # Build URL with query parameters
        params = {
            "ss": city,
            "checkin": checkin,
            "checkout": checkout,
            "group_adults": 2,
            "group_children": 0,
            "no_rooms": 1,
        }
        
        query_string = "&".join([f"{k}={v}" for k, v in params.items()])
        url = f"{self.base_url}{BOOKING_CONFIG['search_endpoint']}?{query_string}"
        
        logger.info(f"Built search URL: {url}")
        return url
    
    def _parse_hotel_card(self, card) -> Optional[Dict]:
        """Parse individual hotel card from HTML"""
        try:
            # Extract hotel name
            name_elem = card.find("div", {"data-testid": "title"})
            if not name_elem:
                return None
            name = name_elem.get_text(strip=True)
            
            # Extract price
            price_elem = card.find("span", {"data-testid": "price-and-discounted-price"})
            if not price_elem:
                # Try alternative price selector
                price_elem = card.find("span", class_=lambda x: x and "prco-valign-middle-helper" in x)
            
            if price_elem:
                price_text = price_elem.get_text(strip=True)
                # Extract numeric value from price string (e.g., "₹5,000" -> 5000)
                price = float(''.join(filter(str.isdigit, price_text.replace(',', ''))))
            else:
                price = 0.0
            
            # Extract rating
            rating_elem = card.find("div", {"data-testid": "review-score"})
            if rating_elem:
                rating_text = rating_elem.find("div", class_=lambda x: x and "review-score-badge" in str(x))
                if rating_text:
                    rating = float(rating_text.get_text(strip=True).split()[0]) / 2  # Convert 10-scale to 5-scale
                else:
                    rating = 0.0
            else:
                rating = 0.0
            
            # Generate a pseudo hotel_id based on name hash
            hotel_id = abs(hash(name)) % 100000
            
            return {
                "hotel_id": hotel_id,
                "name": name,
                "price": price,
                "currency": "INR",  # Default to INR for Indian cities
                "rating": round(rating, 1)
            }
            
        except Exception as e:
            logger.error(f"Error parsing hotel card: {e}")
            return None
    
    def search_hotels(self, city: str, checkin: Optional[str] = None, checkout: Optional[str] = None) -> List[Dict]:
        """
        Search for hotels in a given city
        
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
                logger.info(f"Attempt {attempt + 1}/{self.max_retries} to scrape {city}")
                
                # Make request
                response = requests.get(url, headers=self._get_headers(), timeout=self.timeout)
                response.raise_for_status()
                
                # Parse HTML
                soup = BeautifulSoup(response.content, 'lxml')
                
                # Find hotel cards - Booking.com uses data-testid attributes
                hotel_cards = soup.find_all("div", {"data-testid": "property-card"})
                
                if not hotel_cards:
                    logger.warning(f"No hotel cards found for {city}")
                    return []
                
                # Parse each hotel card
                hotels = []
                for card in hotel_cards[:BOOKING_CONFIG["max_results"]]:
                    hotel_data = self._parse_hotel_card(card)
                    if hotel_data:
                        hotels.append(hotel_data)
                
                logger.info(f"Successfully scraped {len(hotels)} hotels for {city}")
                return hotels
                
            except requests.exceptions.RequestException as e:
                logger.error(f"Request error on attempt {attempt + 1}: {e}")
                if attempt < self.max_retries - 1:
                    time.sleep(self.retry_delay * (attempt + 1))  # Exponential backoff
                else:
                    logger.error(f"Failed to scrape after {self.max_retries} attempts")
                    return []
            
            except Exception as e:
                logger.error(f"Unexpected error: {e}")
                return []
        
        return []


# Simple in-memory cache
class SimpleCache:
    """Simple in-memory cache for hotel data"""
    
    def __init__(self, ttl: int = 3600, max_size: int = 100):
        self.cache = {}
        self.ttl = ttl
        self.max_size = max_size
    
    def get(self, key: str) -> Optional[List[Dict]]:
        """Get cached data if not expired"""
        if key in self.cache:
            data, timestamp = self.cache[key]
            if time.time() - timestamp < self.ttl:
                logger.info(f"Cache hit for key: {key}")
                return data
            else:
                logger.info(f"Cache expired for key: {key}")
                del self.cache[key]
        return None
    
    def set(self, key: str, value: List[Dict]):
        """Set cache data"""
        # Simple LRU: remove oldest if cache is full
        if len(self.cache) >= self.max_size:
            oldest_key = min(self.cache.keys(), key=lambda k: self.cache[k][1])
            del self.cache[oldest_key]
        
        self.cache[key] = (value, time.time())
        logger.info(f"Cached data for key: {key}")
    
    def clear(self):
        """Clear all cache"""
        self.cache.clear()
        logger.info("Cache cleared")


# Global cache instance
hotel_cache = SimpleCache(
    ttl=BOOKING_CONFIG.get("ttl", 3600),
    max_size=BOOKING_CONFIG.get("max_size", 100)
)


def fetch_hotels(city: str, checkin: Optional[str] = None, checkout: Optional[str] = None, use_cache: bool = True) -> List[Dict]:
    """
    Main function to fetch hotel data with caching
    
    Args:
        city: City name to search
        checkin: Check-in date (YYYY-MM-DD format)
        checkout: Check-out date (YYYY-MM-DD format)
        use_cache: Whether to use cached data
        
    Returns:
        List of hotel dictionaries
    """
    # Create cache key
    cache_key = f"{city}_{checkin}_{checkout}"
    
    # Check cache first
    if use_cache:
        cached_data = hotel_cache.get(cache_key)
        if cached_data:
            return cached_data
    
    # Scrape fresh data
    scraper = BookingComScraper()
    hotels = scraper.search_hotels(city, checkin, checkout)
    
    # Cache the results
    if hotels and use_cache:
        hotel_cache.set(cache_key, hotels)
    
    return hotels
