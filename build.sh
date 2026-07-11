#!/usr/bin/env bash
# exit on error
set -o errexit

# Install Python requirements
pip install -r requirements.txt

# Compile static assets
python manage.py collectstatic --no-input

# Apply database migrations
python manage.py migrate
