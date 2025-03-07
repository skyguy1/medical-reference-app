#!/bin/bash
# exit on error
set -o errexit

# Install dependencies
pip install -r requirements.txt

# Initialize the database
python -c "from app import app, db; app.app_context().push(); db.create_all()"

# Import sample data
python import_data.py
