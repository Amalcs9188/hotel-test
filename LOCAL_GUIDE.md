# 🏠 Local Docker Guide

Your Hotel API Scraper is running locally!

## ⚡ Quick Start

The container is already running. You can test it immediately:

### 1. Health Check

```bash
curl http://localhost:8000/
```

**Expected**: `{"status":"ok", ...}`

### 2. Search Hotels (Real Data)

```bash
curl "http://localhost:8000/hotels/search?city=Mumbai" -H "access_token: user_123_secret_key"
```

## 🛠️ Management Commands

**Stop the Scraper:**

```powershell
docker stop hotel-scraper-local
```

**Start the Scraper:**

```powershell
docker start hotel-scraper-local
```

**View Logs (if errors occur):**

```powershell
docker logs -f hotel-scraper-local
```

## 🌐 How to Expose to Internet (Ngrok)

If you need to call this API from another location (e.g., a phone app or another server):

1.  Download **Ngrok**: [https://ngrok.com/download](https://ngrok.com/download)
2.  Run:
    ```powershell
    ngrok http 8000
    ```
3.  Use the `https://....ngrok-free.app` URL provided!
