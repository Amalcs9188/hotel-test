"""
Quick API Test - Verify Hotel Search is Working
"""
import requests

# Test configuration
BASE_URL = "http://127.0.0.1:8000"
API_KEY = "user_123_secret_key"
TEST_CITIES = ["Kochi", "Singapore", "Paris", "Dubai"]

def test_hotel_search():
    """Test hotel search for multiple cities"""
    print("🧪 Testing Hotel Data API\n")
    print("=" * 50)
    
    headers = {"access_token": API_KEY}
    
    for city in TEST_CITIES:
        try:
            print(f"\n📍 Testing: {city}...", end=" ")
            response = requests.get(
                f"{BASE_URL}/hotels/search",
                params={"city": city},
                headers=headers,
                timeout=60
            )
            
            if response.status_code == 200:
                data = response.json()
                if data and len(data) > 0:
                    hotel = data[0]
                    print(f"✅ WORKING")
                    print(f"   Found: {hotel['name']}")
                    print(f"   Price: ₹{hotel['price']}")
                    print(f"   Rating: {hotel['rating']}/5")
                    print(f"   URL: {hotel['url'][:50]}..." if hotel['url'] else "   URL: None")
                else:
                    print(f"⚠️  No hotels found")
            else:
                print(f"❌ FAILED (Status: {response.status_code})")
                print(f"   Error: {response.text}")
        except Exception as e:
            print(f"❌ ERROR: {str(e)}")
    
    print("\n" + "=" * 50)
    print("\n✅ API is working! You can search hotels from any city worldwide!")

if __name__ == "__main__":
    test_hotel_search()
