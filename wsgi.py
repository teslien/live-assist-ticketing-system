#!/usr/bin/env python3
"""
WSGI entry point for production deployment
"""
from app import app, socketio, init_db

if __name__ == "__main__":
    # Initialize database
    init_db()
    
    # For WSGI servers like Gunicorn
    application = socketio
else:
    # Initialize database on import
    init_db()
    application = socketio
