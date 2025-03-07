#!/bin/bash
# exit on error
set -o errexit

echo "Starting build process with enhanced dependency management..."

# Install dependencies with exact versions
echo "Installing dependencies with pinned versions..."
pip install -r requirements.txt

# Verify dependencies
echo "Verifying dependency compatibility..."
python verify_dependencies.py
if [ $? -ne 0 ]; then
    echo "ERROR: Dependency verification failed. Aborting build."
    exit 1
fi

# Create database directory if it doesn't exist
mkdir -p instance

echo "Build completed successfully!"
