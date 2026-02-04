"""
Final test for FabExpress Bright Inn
"""
from scraper_playwright import fetch_hotel_details
import json

url = 'https://www.booking.com/hotel/in/fabexpress-bright-inn.html'
result = fetch_hotel_details(url)

if result:
    print(f"SUCCESS: {result.get('name')}")
    print(f"Amenities found: {len(result.get('amenities', []))}")
    print(f"Reviews found: {len(result.get('reviews', []))}")
    if result.get('reviews'):
        print(f"First review Full: {json.dumps(result['reviews'][0], indent=2)}")
else:
    print("FAILED to fetch details")
