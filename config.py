"""
Configuration settings for Hotel Data API
"""

import os
from typing import List

# API Configuration
API_TITLE = "Hotel Data API"
API_VERSION = "1.0"
API_DESCRIPTION = "Professional hotel search API with real-time data from Booking.com"

# Security Configuration
VALID_API_KEYS: List[str] = [
    "user_123_secret_key",
    "premium_user_key_999"
]

# Scraper Configuration
SCRAPER_CONFIG = {
    "timeout": 30,  # seconds
    "max_retries": 3,
    "retry_delay": 2,  # seconds
    "user_agents": [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    ],
    "headless": True,  # Run browser in headless mode
}

# Cache Configuration
CACHE_CONFIG = {
    "enabled": True,
    "ttl": 3600,  # Time to live in seconds (1 hour)
    "max_size": 100,  # Maximum number of cached items
}

# Booking.com Configuration
BOOKING_CONFIG = {
    "base_url": "https://www.booking.com",
    "search_endpoint": "/searchresults.html",
    "default_checkin_offset": 7,  # days from today
    "default_checkout_offset": 8,  # days from today
    "max_results": 10,  # Maximum number of hotels to return
    "max_reviews": 10,  # Maximum reviews to fetch for hotel details
    "max_photos": 15,  # Maximum photos to fetch
    "detail_timeout": 45,  # Timeout for detail page scraping (seconds)
}

# Fallback to mock data if scraping fails
ENABLE_MOCK_FALLBACK = False
