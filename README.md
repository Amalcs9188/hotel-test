# Hotel Data API 🏨

A professional FastAPI-based hotel search API with API key authentication, designed to be sellable on platforms like RapidAPI.

## Features

- 🔐 **Secure API Key Authentication** - Header-based token validation
- 📊 **Structured JSON Responses** - Pydantic models ensure data consistency
- 🌍 **Multi-City Support** - Search hotels across multiple cities
- 📚 **Auto-Generated Documentation** - Interactive Swagger UI and ReDoc
- ⚡ **Fast & Lightweight** - Built with FastAPI for high performance
- 🛡️ **Proper Error Handling** - Clear HTTP status codes and error messages

## Quick Start

### Installation

```bash
pip install fastapi uvicorn requests
```

### Running the Server

```bash
uvicorn main:app --reload
```

The API will be available at:

- **Base URL:** http://127.0.0.1:8000
- **Interactive Docs:** http://127.0.0.1:8000/docs
- **Alternative Docs:** http://127.0.0.1:8000/redoc

## API Endpoints

### 🏠 Root Endpoint

```
GET /
```

Returns API information and available endpoints.

**Response:**

```json
{
  "message": "Welcome to Hotel Data API",
  "version": "1.0",
  "documentation": "/docs",
  "endpoints": {
    "search_hotels": "/hotels/search?city={city_name}"
  }
}
```

### 🔍 Search Hotels

```
GET /hotels/search?city={city_name}
```

**Authentication Required:** Yes (API Key in header)

**Headers:**

```
access_token: your_api_key_here
```

**Parameters:**

- `city` (required): City name (e.g., Mumbai, Delhi, Bangalore)

**Response (200 OK):**

```json
[
  {
    "hotel_id": 101,
    "name": "Taj Mahal Palace",
    "price": 250.0,
    "currency": "USD",
    "rating": 4.9
  }
]
```

**Error Responses:**

- `403 Forbidden` - Invalid or missing API key
- `404 Not Found` - No hotels found for the specified city

## Authentication

This API uses header-based API key authentication. Include your API key in the `access_token` header with every request.

### Valid API Keys (for testing)

```
user_123_secret_key
premium_user_key_999
```

### Example Requests

**PowerShell:**

```powershell
Invoke-WebRequest -Uri "http://127.0.0.1:8000/hotels/search?city=Mumbai" `
  -Headers @{"access_token"="user_123_secret_key"} `
  -UseBasicParsing
```

**Python:**

```python
import requests

url = "http://127.0.0.1:8000/hotels/search"
headers = {"access_token": "user_123_secret_key"}
params = {"city": "Mumbai"}

response = requests.get(url, headers=headers, params=params)
print(response.json())
```

**cURL:**

```bash
curl -X GET "http://127.0.0.1:8000/hotels/search?city=Mumbai" \
  -H "access_token: user_123_secret_key"
```

## Supported Cities

Currently supports mock data for:

- Mumbai
- Delhi
- Bangalore

## Project Structure

```
hotel-data-api/
├── main.py           # Main FastAPI application
└── README.md         # This file
```

## Next Steps

### For Production Deployment

1. **Replace Mock Data** - Integrate real hotel data sources (web scraping or third-party APIs)
2. **Database Integration** - Store API keys and hotel data in a database
3. **Rate Limiting** - Implement request limits per API key
4. **Caching** - Add Redis/Memcached for faster responses
5. **Deployment** - Deploy to AWS Lambda, Google Cloud Run, or Heroku
6. **Monitoring** - Add logging and analytics

### For RapidAPI Integration

1. Create a RapidAPI account
2. Configure pricing tiers (free, basic, premium)
3. Add comprehensive documentation
4. Set up payment processing
5. Publish your API

## Security Notes

⚠️ **Important:**

- Never commit API keys to version control
- Use environment variables for sensitive data in production
- Implement rate limiting to prevent abuse
- Use HTTPS in production environments

## License

This project is provided as-is for educational and commercial purposes.

## Support

For questions or issues, please open an issue in the repository.

---

Built with ❤️ using [FastAPI](https://fastapi.tiangolo.com/)
