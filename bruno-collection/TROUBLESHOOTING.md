# 🔧 Fixing "Invalid or missing API key" Error

## The Problem

You're getting: `{"detail": "Invalid or missing API key"}`

## ✅ Solution: Select the Environment

### Step 1: Select "Local" Environment

1. Look at the **top-right corner** of Bruno
2. Find the **environment dropdown** (might say "No Environment")
3. Click it and select **"Local"**

![Environment Selection](https://i.imgur.com/example.png)

### Step 2: Verify Environment Variables

After selecting "Local", the variables should be:

- `{{base_url}}` → `http://127.0.0.1:8000`
- `{{api_key}}` → `user_123_secret_key`

### Step 3: Test Again

Run any request - it should work now!

## 🔍 How to Verify It's Working

### Check the Headers Tab:

1. Click on any request
2. Go to **"Headers"** tab
3. You should see:
   - **Name**: `access_token`
   - **Value**: `user_123_secret_key` (not `{{api_key}}`)

If you still see `{{api_key}}` in the value, the environment isn't selected!

## 🎯 Quick Test

### Option 1: Use Request #13 (Kochi - Verified)

This is confirmed working - just make sure "Local" environment is selected.

### Option 2: Hardcode the API Key (Temporary)

If environment selection isn't working:

1. Go to **Headers** tab
2. Change `access_token` value from `{{api_key}}` to `user_123_secret_key`
3. This bypasses the environment variable

## ✅ Expected Working Response

Once the environment is selected, you should get:

```json
{
  "hotel_id": 34607,
  "name": "Treebo Time Square Marine Drive",
  "price": 2585.0,
  "currency": "INR",
  "rating": 3.8,
  "url": "https://www.booking.com/hotel/in/time-square-cochin-688001.html"
}
```

## 🆘 Still Not Working?

### Check Server is Running:

1. Make sure `uvicorn main:app --reload` is running
2. Visit http://127.0.0.1:8000 in browser - should show API info

### Valid API Keys:

- `user_123_secret_key` ✅
- `premium_user_key_999` ✅

Any other key will fail with 403 Forbidden.

## 🎉 Once It Works

You'll be able to:

- Search hotels in any city worldwide
- Get real prices and ratings
- Extract Booking.com URLs
- Fetch full hotel details

The environment selection is the key! Make sure "Local" is selected in the dropdown! 🔑
