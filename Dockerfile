# Use official Playwright image (includes browsers & dependencies)
FROM mcr.microsoft.com/playwright/python:v1.40.0-jammy

# Set working directory
WORKDIR /app

# Install Python dependencies
COPY requirements.txt .


# Copy application code
COPY . .

# Expose port (Railway sets PORT env var)
ENV PORT=8000
EXPOSE $PORT

# Run the application
CMD uvicorn main:app --host 0.0.0.0 --port $PORT
