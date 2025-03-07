#!/bin/bash
# exit on error
set -o errexit

# Upgrade pip first
pip install --upgrade pip

# Install dependencies with explicit version pinning for deployment
pip install -r minimal_requirements.txt

# Print installed packages for debugging
pip list

# Print success message
echo "Build completed successfully!"
