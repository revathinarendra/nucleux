#!/bin/bash

# Ensure pip is available
/usr/bin/python3.9 -m ensurepip --upgrade

# Upgrade pip
/usr/bin/python3.9 -m pip install --upgrade pip

# Install dependencies from requirements.txt
/usr/bin/python3.9 -m pip install -r requirements.txt

# Set up the virtual environment
# Create a virtual environment if it doesn't exist
if [ ! -d "env" ]; then
  /usr/bin/python3.9 -m venv env
fi

# Activate the virtual environment
source env/bin/activate

# Install dependencies in the virtual environment
pip install -r requirements.txt

# Ensure that the static directory exists in the Vercel public folder
mkdir -p /vercel/path0/public/static

# Collect static files to the correct directory
python manage.py collectstatic --noinput

# Apply database migrations
python manage.py makemigrations
python manage.py migrate

# Deactivate the virtual environment
deactivate
