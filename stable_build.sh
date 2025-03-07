#!/bin/bash
# exit on error
set -o errexit

echo "Starting stable build process..."

# Upgrade pip first
pip install --upgrade pip

# Install dependencies without pandas to ensure stable deployment
pip install -r stable_requirements.txt

# Print installed packages for debugging
pip list

# Print success message
echo "Stable build completed successfully!"
