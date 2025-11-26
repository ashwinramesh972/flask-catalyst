# ───────────────────────────────
# flask-catalyst — Dockerfile
# ───────────────────────────────
FROM python:3.12-slim

# Prevent Python buffering
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Create app directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first (better caching)
COPY requirements/base.txt .
RUN pip install --no-cache-dir -r base.txt

# Copy project
COPY . .

# Create instance folder
RUN mkdir -p instance

# Expose port
EXPOSE 5000

# Run the app
CMD ["python", "main.py"]