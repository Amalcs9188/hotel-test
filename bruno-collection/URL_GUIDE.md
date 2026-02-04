# Hotel URL Extraction - Quick Guide

## ✅ URLs Now Included in Search Results!

The hotel search endpoint now returns **Booking.com URLs** for each hotel, making it easy to fetch detailed information.

### Example Response:

```json
{
  "hotel_id": 86566,
  "name": "Atlantiis Suites By Signature Stayz",
  "price": 5879.0,
  "currency": "INR",
  "rating": 4.2,
  "url": "https://www.booking.com/hotel/in/atlantiis-suites-by-signature-stayz.html"
}
```

## 🔄 Workflow: Search → Details

### Step 1: Search for Hotels

```bash
GET /hotels/search?city=Delhi
```

### Step 2: Copy the URL

From the response, copy the `url` field of any hotel.

### Step 3: Get Full Details

```bash
GET /hotels/details?hotel_url=<copied_url>
```

## 📝 Example in Bruno

1. **Run "Search Hotels - Delhi"**
2. **Copy a hotel URL** from the response
3. **Open "Get Hotel Details - From Search Result"**
4. **Paste the URL** in the `hotel_url` parameter
5. **Send** to get full details!

## 💡 What You Get

**From Search (`/hotels/search`):**

- Hotel ID
- Name
- Price
- Rating
- **URL** ← Use this!

**From Details (`/hotels/details`):**

- Everything from search, PLUS:
- Amenities
- Reviews
- Photos
- Room types
- Policies
- Contact info

## ⚠️ Note About Hotel IDs

Currently, the hotel ID is **generated from the hotel name** (not from Booking.com). This means:

❌ **Cannot use hotel ID** to fetch details (no ID-to-URL mapping)
✅ **Must use the URL** from search results

### Why?

Booking.com doesn't expose hotel IDs in the HTML. The URL is the unique identifier.

## 🎯 Best Practice

**Always use the workflow:**

1. Search → Get list with URLs
2. Pick a hotel → Copy its URL
3. Get details → Use the URL

This ensures you're fetching details for the exact hotel from the search results!
