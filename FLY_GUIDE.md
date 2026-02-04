# ✈️ Fly.io Deployment Guide

Your Hotel API Scraper is being deployed to Fly.io!

## 🔗 Quick Links

- **Live API**: `https://hotel-scraper-amal.fly.dev`
- **Status Check**: `https://hotel-scraper-amal.fly.dev/`
- **Dashboard**: [https://fly.io/apps/hotel-scraper-amal](https://fly.io/apps/hotel-scraper-amal)

## ⚡ Verification

Once deployment completes, verify it works:

```powershell
curl "https://hotel-scraper-amal.fly.dev/hotels/search?city=Mumbai" -H "access_token: user_123_secret_key"
```

## 🛠️ Management

**Check Status:**

```powershell
fly status
```

**View Logs:**

```powershell
fly logs
```

**Restart App:**

```powershell
fly apps restart hotel-scraper-amal
```

**Scale Memory (if needed):**
Currently set to **1GB RAM** (perfect for Playwright).

```powershell
fly scale memory 512
```

## ⚠️ Notes

- The app will automatically suspend if idle (to save credits) and wake up on request (might take 5-10s for first request).
- If you see `502 Bad Gateway`, check logs (`fly logs`). It usually means the app crashed or is starting up.
