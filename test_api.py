"""
Test script for Hotel Data API
Demonstrates how to use the API with different scenarios
"""

import requests
import json

# API Configuration
BASE_URL = "http://127.0.0.1:8000"
VALID_API_KEY = "user_123_secret_key"
INVALID_API_KEY = "wrong_key"

def print_response(title, response):
    """Pretty print API response"""
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}")
    print(f"Status Code: {response.status_code}")
    print(f"Response:")
    try:
        print(json.dumps(response.json(), indent=2))
    except:
        print(response.text)

def test_root_endpoint():
    """Test the root endpoint (no auth required)"""
    response = requests.get(f"{BASE_URL}/")
    print_response("Test 1: Root Endpoint (No Auth)", response)

def test_without_api_key():
    """Test hotel search without API key (should fail)"""
    response = requests.get(f"{BASE_URL}/hotels/search", params={"city": "Mumbai"})
    print_response("Test 2: Search Without API Key (Should Fail)", response)

def test_with_invalid_api_key():
    """Test hotel search with invalid API key (should fail)"""
    headers = {"access_token": INVALID_API_KEY}
    response = requests.get(f"{BASE_URL}/hotels/search", params={"city": "Mumbai"}, headers=headers)
    print_response("Test 3: Search With Invalid API Key (Should Fail)", response)

def test_with_valid_api_key():
    """Test hotel search with valid API key (should succeed)"""
    headers = {"access_token": VALID_API_KEY}
    response = requests.get(f"{BASE_URL}/hotels/search", params={"city": "Mumbai"}, headers=headers)
    print_response("Test 4: Search Mumbai With Valid API Key", response)

def test_multiple_cities():
    """Test hotel search for different cities"""
    headers = {"access_token": VALID_API_KEY}
    cities = ["Mumbai", "Delhi", "Bangalore"]
    
    for city in cities:
        response = requests.get(f"{BASE_URL}/hotels/search", params={"city": city}, headers=headers)
        print_response(f"Test 5.{cities.index(city)+1}: Search {city}", response)

def test_invalid_city():
    """Test hotel search for a city with no data"""
    headers = {"access_token": VALID_API_KEY}
    response = requests.get(f"{BASE_URL}/hotels/search", params={"city": "InvalidCity"}, headers=headers)
    print_response("Test 6: Search Invalid City (Should Return 404)", response)

if __name__ == "__main__":
    print("\n" + "="*60)
    print("  HOTEL DATA API - TEST SUITE")
    print("="*60)
    print("\nMake sure the API server is running:")
    print("  uvicorn main:app --reload")
    print("\nStarting tests...\n")
    
    try:
        # Run all tests
        test_root_endpoint()
        test_without_api_key()
        test_with_invalid_api_key()
        test_with_valid_api_key()
        test_multiple_cities()
        test_invalid_city()
        
        print("\n" + "="*60)
        print("  ALL TESTS COMPLETED")
        print("="*60 + "\n")
        
    except requests.exceptions.ConnectionError:
        print("\n❌ ERROR: Could not connect to the API server.")
        print("Please make sure the server is running:")
        print("  uvicorn main:app --reload\n")
    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}\n")
