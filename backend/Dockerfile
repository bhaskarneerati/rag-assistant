FROM python:3.11-slim

WORKDIR /app

# Install system dependencies if needed (e.g., for building some python packages)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements from root
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend code and persisted DB
# Note: Copying backend/app to /app/app
COPY backend/app ./app
# Copying backend/chroma_db to /app/chroma_db (will be created if doesn't exist yet in build)
COPY backend/chroma_db ./chroma_db

# Set environment variables
ENV PYTHONPATH=/app
ENV CHROMA_PATH=/app/chroma_db
ENV PYTHONUNBUFFERED=1

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
