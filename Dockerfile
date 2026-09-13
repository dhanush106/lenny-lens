FROM python:3.11-slim
WORKDIR /app

# Install postgres dependencies
RUN apt-get update && apt-get install -y libpq-dev gcc && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Expose port
EXPOSE 8000

# Apply schema migrations before starting the API. This makes a fresh Compose
# startup reproducible instead of requiring a manual database setup step.
CMD ["sh", "-c", "alembic upgrade head && uvicorn backend.main:app --host 0.0.0.0 --port 8000"]
