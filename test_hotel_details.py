"""
Test script for hotel details endpoint
Demonstrates how to fetch comprehensive hotel information
"""

import requests
import json

# API Configuration
BASE_URL = "http://127.0.0.1:8000"
API_KEY = "user_123_secret_key"

def test_hotel_details():
    """Test fetching detailed hotel information"""
    
    # Example Booking.com hotel URL (Taj Mahal Palace Mumbai)
    hotel_url = "https://www.booking.com/hotel/in/taj-mahal-palace.html"
    
    print("\n" + "="*70)
    print("  TESTING HOTEL DETAILS ENDPOINT")
    print("="*70)
    print(f"\nFetching details for: {hotel_url}")
    print("This may take 20-30 seconds...\n")
    
    headers = {"access_token": API_KEY}
    params = {"hotel_url": hotel_url}
    
    try:
        response = requests.get(
            f"{BASE_URL}/hotels/details",
            headers=headers,
            params=params,
            timeout=60
        )
        
        if response.status_code == 200:
            details = response.json()
            
            print("✅ SUCCESS! Hotel details fetched:\n")
            print(f"📍 Hotel Name: {details['name']}")
            print(f"⭐ Rating: {details['rating']}/5.0")
            print(f"📍 Address: {details.get('address', 'N/A')}")
            
            print(f"\n🏨 Amenities ({len(details.get('amenities', []))}):")
            for amenity in details.get('amenities', [])[:5]:
                print(f"  - {amenity['name']} ({amenity['category']})")
            if len(details.get('amenities', [])) > 5:
                print(f"  ... and {len(details['amenities']) - 5} more")
            
            print(f"\n💬 Reviews ({len(details.get('reviews', []))}):")
            for review in details.get('reviews', [])[:3]:
                print(f"  - {review['reviewer_name']} ({review['rating']}/5.0)")
                print(f"    \"{review['comment'][:100]}...\"")
            
            print(f"\n📸 Photos: {len(details.get('photos', []))} images")
            
            print(f"\n🛏️ Room Types ({len(details.get('room_types', []))}):")
            for room in details.get('room_types', [])[:3]:
                print(f"  - {room['name']}: {room['currency']} {room['price']}")
            
            print(f"\n🕐 Check-in: {details.get('check_in_time', 'N/A')}")
            print(f"🕐 Check-out: {details.get('check_out_time', 'N/A')}")
            
            print("\n" + "="*70)
            print("  FULL JSON RESPONSE")
            print("="*70)
            print(json.dumps(details, indent=2))
            
        else:
            print(f"❌ Error: {response.status_code}")
            print(response.text)
            
    except requests.exceptions.Timeout:
        print("❌ Request timed out. The scraper may be taking longer than expected.")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    print("\n🔍 Hotel Details API Test")
    print("\nMake sure the API server is running:")
    print("  uvicorn main:app --reload\n")
    
    try:
        test_hotel_details()
    except KeyboardInterrupt:
        print("\n\nTest cancelled by user.")
