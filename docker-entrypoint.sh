#!/bin/sh
set -eu

echo "Applying database migrations..."
alembic upgrade head

echo "Applying database seeds..."
python3 -m db.seed

echo "Starting application..."
exec "$@"
