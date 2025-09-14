#!/bin/bash
# Production startup script

echo "Starting Ticketing System..."

# Set production environment
export FLASK_ENV=production
export RENDER=true

# Get port from environment or default to 5000
PORT=${PORT:-5000}

echo "Port: $PORT"
echo "Environment: $FLASK_ENV"

# Start with Gunicorn for production
if command -v gunicorn &> /dev/null; then
    echo "Starting with Gunicorn..."
    exec gunicorn --worker-class eventlet -w 1 --bind 0.0.0.0:$PORT wsgi:application
else
    echo "Gunicorn not found, starting with Python (development mode)..."
    exec python app.py
fi
