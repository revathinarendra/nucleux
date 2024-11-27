#!/bin/bash

# Ensure pip is available
/usr/bin/python3.9 -m ensurepip --upgrade

# Upgrade pip
/usr/bin/python3.9 -m pip install --upgrade pip

# Install dependencies from requirements.txt
/usr/bin/python3.9 -m pip install -r requirements.txt

# Create static and public directories if they don't exist
mkdir -p /vercel/path0/static
mkdir -p /vercel/path0/public/static

# Collect static files
python3.9 manage.py collectstatic --noinput

# Copy collected static files to the public directory
cp -r /vercel/path0/static/* /vercel/path0/public/static/

# Apply database migrations
python3.9 manage.py makemigrations
python3.9 manage.py migrate
