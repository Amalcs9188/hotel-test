# Hotel Data API - Bruno Collection

This is a Bruno API testing collection for the Hotel Data API.

## 📁 Collection Structure

```
bruno-collection/
├── bruno.json                           # Collection config
├── environments/
│   └── Local.bru                        # Environment variables
├── 1. Get API Info.bru                  # Root endpoint
├── 2. Search Hotels - Mumbai.bru        # Search hotels
├── 3. Search Hotels - Delhi with Dates.bru
├── 4. Search Hotels - Bangalore.bru
├── 5. Get Hotel Details - Taj Mahal Palace.bru
├── 6. Test - No API Key (Should Fail).bru
└── 7. Test - Invalid City (Should Return 404).bru
```

## 🚀 How to Use

### 1. Install Bruno

Download from: https://www.usebruno.com/downloads

### 2. Open Collection

1. Open Bruno
2. Click "Open Collection"
3. Navigate to: `c:\Users\amalc\Desktop\hotel test\bruno-collection`
4. Select the folder

### 3. Select Environment

1. Click on the environment dropdown (top right)
2. Select "Local"

### 4. Run Requests

Click on any request in the sidebar and click "Send"

## 📋 Available Requests

### 1. Get API Info

- **Method:** GET
- **URL:** `/`
- **Auth:** None
- **Purpose:** Get API information

### 2. Search Hotels - Mumbai

- **Method:** GET
- **URL:** `/hotels/search?city=Mumbai`
- **Auth:** API Key (header)
- **Purpose:** Search hotels in Mumbai
- **Note:** Takes 15-25 seconds on first request

### 3. Search Hotels - Delhi with Dates

- **Method:** GET
- **URL:** `/hotels/search?city=Delhi&checkin=2026-03-01&checkout=2026-03-05`
- **Auth:** API Key (header)
- **Purpose:** Search hotels with specific dates

### 4. Search Hotels - Bangalore

- **Method:** GET
- **URL:** `/hotels/search?city=Bangalore`
- **Auth:** API Key (header)
- **Purpose:** Search hotels in Bangalore

### 5. Get Hotel Details - Taj Mahal Palace

- **Method:** GET
- **URL:** `/hotels/details?hotel_url=https://www.booking.com/hotel/in/taj-mahal-palace.html`
- **Auth:** API Key (header)
- **Purpose:** Get comprehensive hotel details
- **Note:** Takes 20-30 seconds

### 6. Test - No API Key (Should Fail)

- **Method:** GET
- **URL:** `/hotels/search?city=Mumbai`
- **Auth:** None
- **Expected:** 403 Forbidden

### 7. Test - Invalid City (Should Return 404)

- **Method:** GET
- **URL:** `/hotels/search?city=InvalidCityName123`
- **Auth:** API Key (header)
- **Expected:** 404 Not Found

### 8. Get Hotel Details - From Search Result (NEW!)

- **Method:** GET
- **URL:** `/hotels/details?hotel_url=<url_from_search>`
- **Auth:** API Key (header)
- **Purpose:** Demonstrates the workflow: Search → Copy URL → Get Details
- **Note:** Use the `url` field from any search result

## 🔑 Authentication

All requests (except root endpoint) require an API key in the header:

```
access_token: user_123_secret_key
```

Valid API keys:

- `user_123_secret_key`
- `premium_user_key_999`

## 🌍 Environment Variables

Defined in `environments/Local.bru`:

```
base_url: http://127.0.0.1:8000
api_key: user_123_secret_key
```

## 💡 Tips

### Change Cities

Edit the `city` parameter in any search request to test different cities.

### Change Dates

Edit `checkin` and `checkout` parameters (YYYY-MM-DD format).

### Use URLs from Search Results (NEW!)

**Workflow:**

1. Run any search request (e.g., #2 "Search Hotels - Mumbai")
2. In the response, find the `url` field for any hotel:
   ```json
   {
     "hotel_id": 86566,
     "name": "Atlantiis Suites",
     "url": "https://www.booking.com/hotel/in/atlantiis-suites.html"
   }
   ```
3. Copy the URL
4. Open request #8 "Get Hotel Details - From Search Result"
5. Paste the URL in the `hotel_url` parameter
6. Send to get full details!

### Test Other Hotels

1. Go to Booking.com
2. Find any hotel
3. Copy the URL
4. Paste into the `hotel_url` parameter in request #5

### View Logs

Check the terminal running `uvicorn main:app --reload` to see:

- Scraping progress
- Cache hits/misses
- Errors and warnings

## 🎯 Quick Test Sequence

**Recommended workflow:**

1. **Get API Info** - Verify API is running
2. **Search Hotels - Mumbai** - Test basic search, get hotel list with URLs
3. **Copy a hotel URL** from the response
4. **Get Hotel Details - From Search Result** - Paste the URL to get full details
5. **Test - No API Key** - Verify authentication works
6. **Test - Invalid City** - Verify error handling

**This demonstrates the complete workflow: Search → Extract URL → Get Details**

## 📊 Expected Response Times

| Request                | Time   | Reason               |
| ---------------------- | ------ | -------------------- |
| Get API Info           | <100ms | Simple JSON response |
| Search Hotels (first)  | 15-25s | Real-time scraping   |
| Search Hotels (cached) | <100ms | Cached data          |
| Hotel Details          | 20-30s | Full page scraping   |

## 🐛 Troubleshooting

### "Connection refused"

- Make sure the API is running: `uvicorn main:app --reload`
- Check the base_url in environment variables

### "403 Forbidden"

- Check that `access_token` header is set
- Verify the API key is correct

### "Timeout"

- Hotel details requests can take 30+ seconds
- Increase timeout in Bruno settings

### "No hotels found"

- Try a different city
- Check server logs for scraping errors
- Scraper may be blocked (will fall back to mock data)

## 📝 Notes

- First requests are slower (real scraping)
- Subsequent requests use cache (1 hour TTL)
- Some requests may fall back to mock data if scraping fails
- All responses are in JSON format

Enjoy testing your Hotel Data API! 🎉
