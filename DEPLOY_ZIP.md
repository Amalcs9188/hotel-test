# Deploying Hotel API to AWS Lambda (ZIP Method - No Docker)

This guide shows how to deploy the **basic scraper** (without Playwright) as a simple ZIP file.

## ⚠️ Important Limitations

This method uses the basic scraper (`scraper.py`) which:

- ✅ Can extract: Hotel name, price, rating, basic info
- ❌ Cannot extract: Reviews, detailed amenities, JavaScript-rendered content
- ❌ May fail on: Modern hotel pages that require JavaScript

**If you need full features, use the Docker method instead.**

---

## Prerequisites

1. **AWS CLI** installed and configured (`aws configure`)
2. **Python 3.9+** installed locally
3. An **AWS Account**

---

## Step 1: Prepare the Deployment Package

### 1.1 Create a deployment directory

```powershell
mkdir lambda-deploy
cd lambda-deploy
```

### 1.2 Copy necessary files

```powershell
Copy-Item ..\main.py .
Copy-Item ..\lambda_function.py .
Copy-Item ..\config.py .
Copy-Item ..\scraper.py .
```

### 1.3 Install dependencies to this directory

```powershell
pip install -t . fastapi pydantic mangum requests beautifulsoup4 lxml fake-useragent
```

### 1.4 Create the ZIP file

```powershell
# Compress everything into a ZIP
Compress-Archive -Path * -DestinationPath ..\hotel-api-lambda.zip -Force
cd ..
```

---

## Step 2: Create Lambda Function via AWS Console

1. Go to [AWS Lambda Console](https://console.aws.amazon.com/lambda/)
2. Click **Create function**
3. Choose **Author from scratch**
4. **Function name**: `HotelApiBasic`
5. **Runtime**: Python 3.11
6. **Architecture**: x86_64
7. Click **Create function**

---

## Step 3: Upload the ZIP

1. In the function page, scroll to **Code source**
2. Click **Upload from** → **.zip file**
3. Select `hotel-api-lambda.zip`
4. Click **Save**

---

## Step 4: Configure the Function

### 4.1 Set the Handler

1. Go to **Runtime settings** → **Edit**
2. **Handler**: `lambda_function.handler`
3. Click **Save**

### 4.2 Increase Timeout and Memory

1. Go to **Configuration** → **General configuration** → **Edit**
2. **Memory**: 512 MB
3. **Timeout**: 30 seconds
4. Click **Save**

---

## Step 5: Create a Function URL (for HTTP access)

1. Go to **Configuration** → **Function URL**
2. Click **Create function URL**
3. **Auth type**: NONE (or AWS_IAM if you want authentication)
4. Click **Save**
5. **Copy the Function URL** - this is your API endpoint!

---

## Step 6: Test the API

Use the Function URL you copied:

```powershell
curl "https://YOUR-FUNCTION-URL.lambda-url.us-east-1.on.aws/hotels/search?city=Mumbai" -H "access_token: test_key_12345"
```

---

## Troubleshooting

### "Module not found" error

- Make sure you installed dependencies with `-t .` flag
- Verify all files are in the ZIP root (not in a subfolder)

### "Task timed out after 3.00 seconds"

- Increase the timeout in Configuration → General configuration

### "No hotels found"

- The basic scraper may not work on all hotel pages
- Consider using the Docker method for full Playwright support

---

## Cost Estimate

- **Lambda**: Free for first 1M requests/month
- **Data Transfer**: Free for first 1GB/month
- **Total**: Essentially **free** for moderate usage
