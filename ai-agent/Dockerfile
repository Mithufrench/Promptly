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

# Cognee's relational DB is SQLite and it NEVER creates missing directories
# itself (sqlite only creates the .db file, not its parent folders).
# Cognee's default DB path is <system_root_directory>/databases/cognee_db,
# so that exact subfolder must exist before cognee ever runs.
RUN mkdir -p /app/cognee_data/system/databases /app/cognee_data/data

ENV SYSTEM_ROOT_DIRECTORY=/app/cognee_data/system
ENV DATA_ROOT_DIRECTORY=/app/cognee_data/data

# Create non-root user — chown AFTER creating the cognee dirs above,
# so appuser actually owns them (this was the real root cause:
# cognee's package-relative default lives under site-packages, which
# is owned by root and unwritable by a non-root runtime user)
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

# EXPOSE port - will be overridden by PORT env var at runtime
EXPOSE 8000

# Start application - reads PORT from environment, binds to 0.0.0.0
CMD ["python", "-u", "main.py"]
