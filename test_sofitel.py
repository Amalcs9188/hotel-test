
from scraper_playwright import fetch_hotel_details
import json

url = "https://www.booking.com/hotel/in/sofitel-mumbai-bkc.html"
result = fetch_hotel_details(url)

if result:
    print(f"SUCCESS: {result.get('name')}")
    print(f"Rating: {result.get('rating')}")
    print(f"Reviews: {len(result.get('reviews', []))}")
    for rev in result.get('reviews', []):
        print(f" - {rev['reviewer_name']} (Rating: {rev['rating']}): {rev['comment'][:100]}...")
else:
    print("FAILED")
