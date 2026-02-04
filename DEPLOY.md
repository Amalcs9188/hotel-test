# Deploying Hotel API to AWS Lambda (Containerized)

Because Playwright requires browser binaries, we must deploy this application as a **Container Image** rather than a standard Zip file upload.

## Prerequisites

### Step 0: Install Docker (Critical)

> **If you see `command not found: docker`, you must do this first.**

1. Download **Docker Desktop** from [docker.com/products/docker-desktop](https://www.docker.com/products/docker-desktop/).
2. Install it and **Start the Application** (it must be running in the system tray).
3. Restart your terminal/VS Code to refresh your `PATH`.
4. Verify by running: `docker --version`.

### Prerequisites for AWS

1. **AWS CLI** installed and configured (`aws configure`).
2. An **AWS Account** with permissions for ECR and Lambda.

## Step 1: Create an ECR Repository

Create a repository to store your Docker image.

```bash
aws ecr create-repository --repository-name hotel-api-scraper --region us-east-1
```

_Note: Replace `us-east-1` with your preferred region._

## Step 2: Build the Docker Image

Build the image locally.

```bash
docker build -t hotel-api-scraper .
```

## Step 3: Login to ECR

Retrieve the login password and pipe it to Docker login.

```bash
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin <YOUR_ACCOUNT_ID>.dkr.ecr.us-east-1.amazonaws.com
```

_Replace `<YOUR_ACCOUNT_ID>` with your actual AWS Account ID (found in AWS Console)._

## Step 4: Tag & Push the Image

Tag your local image to match the ECR repository URL.

```bash
docker tag hotel-api-scraper:latest <YOUR_ACCOUNT_ID>.dkr.ecr.us-east-1.amazonaws.com/hotel-api-scraper:latest
docker push <YOUR_ACCOUNT_ID>.dkr.ecr.us-east-1.amazonaws.com/hotel-api-scraper:latest
```

## Step 5: Create/Update Lambda Function

1. Go to the **AWS Lambda Console**.
2. Click **Create function**.
3. Select **Container image**.
4. Name: `HotelApiScraper`.
5. Container image URI: Click **Browse images** and select the image you just pushed.
6. **Architecture**: Select `x86_64` (since our base image is x86).
7. Click **Create function**.

## Step 6: Critical Configuration

Once the function is created, go to **Configuration** > **General configuration** and Edit:

- **Memory**: Set to at least **1024 MB** (Playwright is memory intensive).
- **Timeout**: Set to **1 Minute 30 Seconds** (Scraping takes ~20s).
- **Ephemeral storage**: 512MB (default) is fine.

## Summary of Commands

```bash
# 1. Login
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin <ACCOUNT_ID>.dkr.ecr.us-east-1.amazonaws.com

# 2. Build
docker build --platform linux/amd64 -t hotel-api-scraper .

# 3. Tag
docker tag hotel-api-scraper:latest <ACCOUNT_ID>.dkr.ecr.us-east-1.amazonaws.com/hotel-api-scraper:latest

# 4. Push
docker push <ACCOUNT_ID>.dkr.ecr.us-east-1.amazonaws.com/hotel-api-scraper:latest
```
