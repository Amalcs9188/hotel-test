"""
Test hotel details endpoint
"""
import requests
import time

url = "http://127.0.0.1:8000/hotels/details"
headers = {"access_token": "user_123_secret_key"}
params = {"hotel_url": "https://www.booking.com/hotel/in/the-taj-mahal-palace-mumbai.html"}

print("Testing hotel details API...")
print(f"URL: {url}")
print(f"Hotel URL: {params['hotel_url']}")
print("\nRunning API call...")
start_time = time.time()
response = requests.get(url, headers=headers, params=params, timeout=60)
end_time = time.time()

duration = end_time - start_time
print(f"Time Taken: {duration:.2f} seconds")

print(f"Status Code: {response.status_code}")

if response.status_code == 200:
    data = response.json()
    print(f"\nHotel: {data['name']}")
    print(f"Rating: {data['rating']}")
    print(f"Address: {data.get('address', 'N/A')}")
    print(f"\nAmenities: {len(data.get('amenities', []))}")
    print(f"Reviews: {len(data.get('reviews', []))}")
    print(f"Photos: {len(data.get('photos', []))}")
    print(f"Room Types: {len(data.get('room_types', []))}")
    
    if data.get('reviews'):
        print("\nFirst 3 reviews:")
        for i, review in enumerate(data['reviews'][:3], 1):
            print(f"\n{i}. {review['reviewer_name']} - Rating: {review['rating']}")
            print(f"   {review['comment'][:100]}...")
    else:
        print("\n⚠️ No reviews found!")
        
    # Save full response for inspection
    import json
    with open("hotel_details_response.json", "w") as f:
        json.dump(data, f, indent=2)
    print("\n✓ Full response saved to hotel_details_response.json")
else:
    print(f"Error: {response.text}")
