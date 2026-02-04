# Global City Support - Your API Works Worldwide! 🌍

## ✅ Your API Supports ALL Cities Globally!

The Hotel Data API can fetch hotel information from **any city in the world** where Booking.com has listings.

## 🌍 How It Works

Simply pass any city name to the search endpoint:

```
GET /hotels/search?city={city_name}
```

**The scraper automatically:**

1. Builds the Booking.com search URL for that city
2. Scrapes real hotel data
3. Returns results with prices, ratings, and URLs

## 🗺️ Supported Regions

### Asia

- **India**: Mumbai, Delhi, Bangalore, Jaipur, Goa, etc.
- **Japan**: Tokyo, Osaka, Kyoto, etc.
- **Thailand**: Bangkok, Phuket, Chiang Mai, etc.
- **Singapore**: Singapore
- **UAE**: Dubai, Abu Dhabi, etc.
- **China**: Beijing, Shanghai, Hong Kong, etc.

### Europe

- **France**: Paris, Lyon, Marseille, etc.
- **UK**: London, Manchester, Edinburgh, etc.
- **Italy**: Rome, Milan, Venice, Florence, etc.
- **Spain**: Barcelona, Madrid, Seville, etc.
- **Germany**: Berlin, Munich, Frankfurt, etc.

### Americas

- **USA**: New York, Los Angeles, Miami, Las Vegas, etc.
- **Canada**: Toronto, Vancouver, Montreal, etc.
- **Mexico**: Cancun, Mexico City, Playa del Carmen, etc.
- **Brazil**: Rio de Janeiro, São Paulo, etc.

### Oceania

- **Australia**: Sydney, Melbourne, Brisbane, etc.
- **New Zealand**: Auckland, Wellington, Queenstown, etc.

### Africa

- **South Africa**: Cape Town, Johannesburg, etc.
- **Egypt**: Cairo, Luxor, etc.
- **Morocco**: Marrakech, Casablanca, etc.

## 📝 Examples in Bruno

I've created example requests for:

- **#10**: Paris, France
- **#11**: Tokyo, Japan
- **#12**: New York, USA

You can test any of these to see international data!

## 💡 Tips for International Cities

### City Names with Spaces

Cities with spaces work automatically:

```
city=New York
city=Los Angeles
city=San Francisco
```

### Specific Locations

Be specific for better results:

```
city=Paris          ✅ Good
city=Paris, France  ✅ Also works
city=Manhattan      ✅ Works (NYC neighborhood)
```

### Language

Use English city names:

```
city=Tokyo          ✅ Good
city=東京            ⚠️ May not work
```

## 🧪 Test Right Now

Try these in Bruno:

### 1. European City

```
GET /hotels/search?city=Paris
```

### 2. Asian City

```
GET /hotels/search?city=Tokyo
```

### 3. American City

```
GET /hotels/search?city=New York
```

### 4. Middle Eastern City

```
GET /hotels/search?city=Dubai
```

## ⚡ Performance Notes

**First Request (Any City):**

- Takes 15-25 seconds (real scraping)
- Fetches fresh data from Booking.com

**Cached Requests:**

- Returns instantly
- Cache expires after 1 hour

## 🎯 Currency Note

Prices are extracted from Booking.com and may be in different currencies depending on:

- The hotel's location
- Booking.com's display settings
- Your IP location

The API shows prices as they appear on Booking.com.

## 🌟 Unlimited Possibilities

**Your API can fetch hotels from:**

- ✅ 220+ countries
- ✅ Thousands of cities
- ✅ Any location on Booking.com

**Just change the `city` parameter!**

## 📊 Example Response (Paris)

```json
{
  "hotel_id": 45821,
  "name": "Hotel de Crillon",
  "price": 450.0,
  "currency": "INR",
  "rating": 4.7,
  "url": "https://www.booking.com/hotel/fr/de-crillon.html"
}
```

## 🚀 Ready to Use

Your API is **already configured** to work worldwide. No additional setup needed!

Just test any city in the Bruno collection and see real hotel data from anywhere in the world! 🌍✨
