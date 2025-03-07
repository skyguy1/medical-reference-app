#!/bin/bash
# exit on error
set -o errexit

echo "Starting standalone build process..."

# Install only the essential dependencies
pip install -r requirements.txt

echo "Standalone build completed successfully!"
