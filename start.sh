#!/bin/bash
# Railway startup script - handles dynamic PORT assignment
set -e

echo "🚀 Starting Prompt-to-Prod AI Agent"
echo "PORT: ${PORT:-8000}"
echo "MODEL: ${MODEL:-mixtral-8x7b-32768}"
echo "ENVIRONMENT: ${ENVIRONMENT:-development}"

# Start the application
cd /app
python -u ai-agent/main.py
