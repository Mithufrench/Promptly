FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install dependencies
COPY ai-agent/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY ai-agent/main.py .
COPY ai-agent/config.py .
COPY ai-agent/memory_manager.py .

# Copy frontend files
COPY frontend/ ./frontend/

# Create non-root user
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

# EXPOSE port - will be overridden by PORT env var at runtime
EXPOSE 8000

# Start application - reads PORT from environment, binds to 0.0.0.0
CMD ["python", "-u", "main.py"]
