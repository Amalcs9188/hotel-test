# Use official Playwright image (includes browsers & dependencies)
FROM mcr.microsoft.com/playwright/python:v1.40.0-jammy

# Set working directory
WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt


# Copy application code
COPY . .

# Expose port (Railway sets PORT env var)
# Expose port 8080 (Fly default)
ENV PORT=8080
EXPOSE 8080

# Run the application
CMD python -m uvicorn main:app --host 0.0.0.0 --port 8080
