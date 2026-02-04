"""
Quick test of the hotel search API
"""
import requests

url = "http://127.0.0.1:8000/hotels/search"
headers = {"access_token": "user_123_secret_key"}
params = {"city": "Kochi"}

print("Testing hotel search API...")
print(f"URL: {url}")
print(f"Params: {params}")

response = requests.get(url, headers=headers, params=params)

print(f"\nStatus Code: {response.status_code}")

if response.status_code == 200:
    data = response.json()
    print(f"Found {len(data)} hotels\n")
    for i, hotel in enumerate(data[:3], 1):
        print(f"{i}. {hotel['name']}")
        print(f"   Price: {hotel['currency']} {hotel['price']}")
        print(f"   Rating: {hotel['rating']}")
        print(f"   URL: {hotel.get('url', 'N/A')}")
        print()
else:
    print(f"Error: {response.text}")
