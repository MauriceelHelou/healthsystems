#!/bin/bash
set -e

echo "=========================================="
echo "HealthSystems Platform - Railway Startup"
echo "=========================================="

# Wait for database to be ready
echo "Waiting for database to be ready..."
python -c "
import time
import sys
from sqlalchemy import create_engine
import os

database_url = os.getenv('DATABASE_URL')
max_retries = 30
retry_delay = 2

for i in range(max_retries):
    try:
        engine = create_engine(database_url)
        conn = engine.connect()
        conn.close()
        print('Database is ready!')
        sys.exit(0)
    except Exception as e:
        if i < max_retries - 1:
            print(f'Database not ready yet (attempt {i+1}/{max_retries}), waiting {retry_delay}s...')
            time.sleep(retry_delay)
        else:
            print(f'Failed to connect to database after {max_retries} attempts')
            sys.exit(1)
"

# Run database migrations
echo "Running database migrations..."
python -m alembic upgrade head

# Seed database with initial data (if needed)
echo "Seeding database with mechanism data..."
python scripts/seed_database.py

# Start the application
echo "Starting FastAPI application..."
exec uvicorn api.main:app --host 0.0.0.0 --port ${PORT:-8000} --workers ${WORKERS:-4}
