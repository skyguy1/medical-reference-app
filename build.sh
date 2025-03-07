#!/bin/bash
# exit on error
set -o errexit

# Install dependencies
pip install flask gunicorn

# Print success message
echo "Build completed successfully!"
