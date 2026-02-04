"""
Hotel Data API - Main Application
Professional hotel search API with real-time data from Booking.com
"""

from fastapi import FastAPI, HTTPException, Depends, Header
from pydantic import BaseModel
from typing import List, Optional
import logging

# Import configuration and scraper
from config import API_TITLE, API_VERSION, API_DESCRIPTION, VALID_API_KEYS, ENABLE_MOCK_FALLBACK
from scraper import fetch_hotels  # Basic scraper

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title=API_TITLE,
    version=API_VERSION,
    description=API_DESCRIPTION
)

# --- 1. MODELS ---
class HotelResponse(BaseModel):
    hotel_id: int
    name: str
    price: float
    currency: str
    rating: float
    url: Optional[str] = None

# --- 2. AUTHENTICATION ---
async def get_api_key(access_token: str = Header(None, alias="access_token")):
    """Validate API key from header"""
    if not access_token or access_token not in VALID_API_KEYS:
        raise HTTPException(status_code=403, detail="Invalid or missing API key")
    return access_token

# --- 3. DATA FETCHING LOGIC ---
def fetch_hotel_data_mock(city: str):
    """Return mock hotel data for testing"""
    logger.warning(f"Using mock data for {city}")
    if city.lower() == "mumbai":
        return [
            {"hotel_id": 101, "name": "Taj Mahal Palace", "price": 250.00, "currency": "USD", "rating": 4.9},
            {"hotel_id": 102, "name": "Trident Nariman Point", "price": 180.00, "currency": "USD", "rating": 4.5}
        ]
    elif city.lower() == "delhi":
        return [
            {"hotel_id": 201, "name": "The Leela Palace New Delhi", "price": 300.00, "currency": "USD", "rating": 4.8},
            {"hotel_id": 202, "name": "The Oberoi", "price": 275.00, "currency": "USD", "rating": 4.7}
        ]
    elif city.lower() == "bangalore":
        return [
            {"hotel_id": 301, "name": "ITC Gardenia", "price": 200.00, "currency": "USD", "rating": 4.6},
            {"hotel_id": 302, "name": "The Ritz-Carlton", "price": 220.00, "currency": "USD", "rating": 4.7}
        ]
    return []

def fetch_hotel_data_real(city: str, checkin: Optional[str] = None, checkout: Optional[str] = None):
    """Fetch real hotel data from Booking.com using basic scraper"""
    try:
        logger.info(f"Fetching hotel data for {city} using basic scraper")
        
        # Use basic scraper (Lambda ZIP compatible)
        hotels = fetch_hotels(city, checkin, checkout, use_cache=True)
        
        if hotels:
            logger.info(f"✅ Successfully fetched {len(hotels)} hotels for {city}")
            return hotels
        
        # Fallback to mock data if enabled
        logger.warning(f"No hotels found for {city}, using mock data fallback")
        if ENABLE_MOCK_FALLBACK:
            return fetch_hotel_data_mock(city)
        return []
            
    except Exception as e:
        logger.error(f"Error fetching hotel data: {e}")
        if ENABLE_MOCK_FALLBACK:
            logger.info("Using mock data due to error")
            return fetch_hotel_data_mock(city)
        return []

# --- NEW: Hotel Details Models ---
class HotelAmenity(BaseModel):
    category: str
    name: str

class HotelReview(BaseModel):
    reviewer_name: str
    rating: float
    comment: str
    date: Optional[str] = None

class HotelPhoto(BaseModel):
    url: str
    caption: Optional[str] = None

class RoomType(BaseModel):
    name: str
    price: float
    currency: str
    max_occupancy: Optional[int] = None

class HotelDetails(BaseModel):
    hotel_id: int
    name: str
    rating: float
    address: Optional[str] = None
    description: Optional[str] = None
    amenities: List[HotelAmenity] = []
    reviews: List[HotelReview] = []
    photos: List[HotelPhoto] = []
    room_types: List[RoomType] = []
    check_in_time: Optional[str] = None
    check_out_time: Optional[str] = None
    policies: Optional[str] = None
    contact_phone: Optional[str] = None
    contact_email: Optional[str] = None

# --- 4. THE ENDPOINT ---
@app.get("/hotels/search", response_model=list[HotelResponse])
async def search_hotels(
    city: str,
    checkin: Optional[str] = None,
    checkout: Optional[str] = None,
    api_key: str = Depends(get_api_key) # This locks the endpoint
):
    """
    Search for hotels in a specific city using real-time data from Booking.com.
    
    **Authentication**: Include your API key in the `access_token` header.
    
    **Parameters**:
    - **city**: The city name to search for hotels (e.g., Mumbai, Delhi, Bangalore)
    - **checkin**: Check-in date in YYYY-MM-DD format (optional, defaults to 7 days from today)
    - **checkout**: Check-out date in YYYY-MM-DD format (optional, defaults to 8 days from today)
    
    **Returns**: A list of hotels with their details including price and rating.
    
    **Note**: Data is cached for 1 hour to improve performance.
    """
    logger.info(f"API request for city: {city}, checkin: {checkin}, checkout: {checkout}")
    
    # Run the scraper in a thread pool to avoid async issues with Playwright Sync API
    import asyncio
    from concurrent.futures import ThreadPoolExecutor
    
    loop = asyncio.get_event_loop()
    with ThreadPoolExecutor() as executor:
        results = await loop.run_in_executor(executor, fetch_hotel_data_real, city, checkin, checkout)
    
    if not results:
        raise HTTPException(status_code=404, detail="No hotels found for this city")
        
    return results

# --- 5. ROOT ENDPOINT ---
@app.get("/")
async def root():
    """
    Welcome endpoint for the Hotel Data API.
    """
    return {
        "message": "Welcome to Hotel Data API",
        "version": API_VERSION,
        "endpoints": {
            "search_hotels": "/hotels/search?city={city_name}&checkin={YYYY-MM-DD}&checkout={YYYY-MM-DD}",
            "hotel_details": "/hotels/details?hotel_url={booking_url}"
        },
        "features": [
            "Real-time hotel data from Booking.com",
            "API key authentication",
            "Automatic caching (1 hour TTL)",
            "Fallback to mock data if scraping fails"
        ]
    }

# Trigger reload
