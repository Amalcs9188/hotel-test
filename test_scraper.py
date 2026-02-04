"""
Test script to verify the web scraper functionality
"""

import sys
import logging
from scraper import BookingComScraper, fetch_hotels

# Setup logging to see what's happening
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

def test_scraper_direct():
    """Test the scraper directly"""
    print("\n" + "="*60)
    print("  Testing Booking.com Scraper Directly")
    print("="*60 + "\n")
    
    scraper = BookingComScraper()
    
    # Test with Mumbai
    print("Testing: Mumbai")
    print("-" * 60)
    hotels = scraper.search_hotels("Mumbai")
    
    if hotels:
        print(f"✅ Successfully scraped {len(hotels)} hotels!")
        for i, hotel in enumerate(hotels[:3], 1):
            print(f"\n{i}. {hotel['name']}")
            print(f"   Price: {hotel['currency']} {hotel['price']}")
            print(f"   Rating: {hotel['rating']}/5.0")
    else:
        print("❌ No hotels found - scraper may have failed")
        print("This is likely due to:")
        print("  1. Booking.com's anti-bot protection")
        print("  2. Network issues")
        print("  3. HTML structure changes")
        print("\nThe API will fall back to mock data in this case.")

def test_fetch_hotels():
    """Test the main fetch_hotels function with caching"""
    print("\n" + "="*60)
    print("  Testing fetch_hotels() Function")
    print("="*60 + "\n")
    
    print("First call (should scrape):")
    hotels = fetch_hotels("Delhi", use_cache=True)
    print(f"Result: {len(hotels)} hotels\n")
    
    print("Second call (should use cache):")
    hotels = fetch_hotels("Delhi", use_cache=True)
    print(f"Result: {len(hotels)} hotels (cached)\n")

if __name__ == "__main__":
    print("\n🔍 Hotel Scraper Test Suite\n")
    
    try:
        test_scraper_direct()
        test_fetch_hotels()
        
        print("\n" + "="*60)
        print("  Test Complete")
        print("="*60)
        print("\n💡 Note: If scraping failed, the API will automatically")
        print("   use mock data as a fallback. This is expected behavior.")
        print("\n")
        
    except Exception as e:
        print(f"\n❌ Error during testing: {e}")
        import traceback
        traceback.print_exc()
