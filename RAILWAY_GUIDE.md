# Railway Deployment Guide

Your Hotel API Scraper is deployed on Railway! 🚂

## 🔗 Quick Links

- **Live API**: [https://hotel-scraper-production-6b8e.up.railway.app](https://hotel-scraper-production-6b8e.up.railway.app)
- **Status Check**: [https://hotel-scraper-production-6b8e.up.railway.app/](https://hotel-scraper-production-6b8e.up.railway.app/)
- **Dashboard**: [https://railway.com/project/381cbb70-1b0c-4015-a922-501aa7b6ba00](https://railway.com/project/381cbb70-1b0c-4015-a922-501aa7b6ba00)

## 🛠️ Debugging "Application Not Found"

If you see a 404 "Application Not Found" error, it means the app failed to start.

1.  **Open the Dashboard link** above.
2.  Click on the **Service** card (e.g., "hotel-scraper").
3.  Click on the **Deployments** tab.
4.  Click on the latest deployment to see **Build Logs** and \*\*Deploy Logs`.

### Common Errors:

- **Build Failed**: Check Build Logs. Usually a dependency issue.
- **Crashed**: Check Deploy Logs. Look for "Exit Code 1" or Python tracebacks.

## 🚀 How to Update

To update the code, simply run:

```powershell
railway up
```

This pushes your local changes to Railway.

## 🧪 Testing

Once active, test with:

```powershell
curl "https://hotel-scraper-production-6b8e.up.railway.app/hotels/search?city=Mumbai" -H "access_token: user_123_secret_key"
```
