"""
Check Makam Holiday Home for reviews
"""
from scraper_playwright import fetch_hotel_details
import json

url = 'https://www.booking.com/hotel/in/makam-holiday-home-muzhakkunnu.html'
result = fetch_hotel_details(url)

if result:
    print(f"SUCCESS: {result.get('name')}")
    print(f"Amenities: {len(result.get('amenities', []))}")
    print(f"Reviews: {len(result.get('reviews', []))}")
    for rev in result.get('reviews', [])[:3]:
        print(f" - {rev['reviewer_name']}: {rev['comment'][:50]}")
else:
    print("FAILED")
