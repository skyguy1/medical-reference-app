#!/bin/bash
# exit on error
set -o errexit

echo "Starting isolated build process..."

# Upgrade pip first
pip install --upgrade pip

# Install only the minimal dependencies needed
pip install -r isolated_requirements.txt

# Print installed packages for debugging
pip list

# Print success message
echo "Isolated build completed successfully!"
