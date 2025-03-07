#!/bin/bash
# exit on error
set -o errexit

# Make sure the script is executable
chmod +x build.sh

pip install --upgrade pip
pip install -r requirements.txt

# Create database tables
python -c "import os; from app import app, db; app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL'); app.app_context().push(); db.create_all()"
