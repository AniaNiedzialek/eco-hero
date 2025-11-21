# Use a slim Python image
FROM python:3.11-slim

# Install OS deps you might need (safe to keep; adjust later if unneeded)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential curl unzip \
    && rm -rf /var/lib/apt/lists/*

# Set workdir
WORKDIR /app

# Copy Python deps first (better layer caching)
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy your backend code
COPY . /app

# Railway sets PORT env var. FastAPI must bind to that port.
ENV PORT=8080

# Start FastAPI in production (Gunicorn + Uvicorn worker)

CMD exec gunicorn -k uvicorn.workers.UvicornWorker -b :$PORT main:app
