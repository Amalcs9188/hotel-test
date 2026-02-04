# Bruno API Testing Collection - Quick Start

## ✅ Collection Created!

Your Bruno collection is ready at:

```
c:\Users\amalc\Desktop\hotel test\bruno-collection\
```

## 📦 What's Included

### 7 Ready-to-Use Requests:

1. **Get API Info** - Test root endpoint
2. **Search Hotels - Mumbai** - Basic hotel search
3. **Search Hotels - Delhi with Dates** - Search with check-in/out dates
4. **Search Hotels - Bangalore** - Another city example
5. **Get Hotel Details - Taj Mahal Palace** - Comprehensive hotel info
6. **Test - No API Key** - Verify authentication (should fail)
7. **Test - Invalid City** - Test error handling (should 404)

### Environment Variables:

- `base_url`: http://127.0.0.1:8000
- `api_key`: user_123_secret_key

## 🚀 How to Use

### Step 1: Install Bruno

Download from: https://www.usebruno.com/downloads

### Step 2: Open Collection

1. Open Bruno
2. Click **"Open Collection"**
3. Navigate to: `c:\Users\amalc\Desktop\hotel test\bruno-collection`
4. Click "Select Folder"

### Step 3: Select Environment

- Click environment dropdown (top right)
- Select **"Local"**

### Step 4: Run Requests

- Click any request in the sidebar
- Click **"Send"** button
- View response in the panel

## 🎯 Quick Test

**Recommended order:**

1. Get API Info (instant)
2. Search Hotels - Mumbai (15-25 seconds first time)
3. Get Hotel Details (20-30 seconds)

## 💡 Tips

### Change Cities

Edit the `city` parameter to test:

- Mumbai, Delhi, Bangalore
- Goa, Jaipur, Pune
- Any Indian city

### Change Dates

Format: `YYYY-MM-DD`

```
checkin: 2026-03-01
checkout: 2026-03-05
```

### Test Other Hotels

1. Go to Booking.com
2. Find any hotel
3. Copy the URL
4. Paste in request #5's `hotel_url` parameter

## 📊 Expected Response Times

| Request         | Time   | Notes            |
| --------------- | ------ | ---------------- |
| API Info        | <100ms | Simple response  |
| Search (first)  | 15-25s | Real scraping    |
| Search (cached) | <100ms | From cache       |
| Hotel Details   | 20-30s | Full page scrape |

## 🔑 Authentication

All requests use the header:

```
access_token: user_123_secret_key
```

Valid keys:

- `user_123_secret_key`
- `premium_user_key_999`

## 📝 File Structure

```
bruno-collection/
├── bruno.json                    # Collection config
├── environments/
│   └── Local.bru                 # Environment vars
├── 1. Get API Info.bru
├── 2. Search Hotels - Mumbai.bru
├── 3. Search Hotels - Delhi with Dates.bru
├── 4. Search Hotels - Bangalore.bru
├── 5. Get Hotel Details - Taj Mahal Palace.bru
├── 6. Test - No API Key (Should Fail).bru
├── 7. Test - Invalid City (Should Return 404).bru
└── README.md                     # Full documentation
```

## 🐛 Troubleshooting

**"Connection refused"**

- Make sure API is running: `uvicorn main:app --reload`

**"403 Forbidden"**

- Check `access_token` header is set
- Verify API key is correct

**"Timeout"**

- Hotel details can take 30+ seconds
- Increase timeout in Bruno settings

**"No hotels found"**

- Try a different city
- Check server logs for errors

## 🎉 You're Ready!

Open Bruno and start testing your Hotel Data API!

For detailed documentation, see `README.md` in the collection folder.
