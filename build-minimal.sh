#!/bin/bash
# exit on error
set -o errexit

echo "Starting minimal build process..."

# Install only the essential dependencies
pip install -r requirements-minimal.txt

echo "Minimal build completed successfully!"
