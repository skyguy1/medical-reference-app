#!/bin/bash
# exit on error
set -o errexit

# Install dependencies
pip install -r requirements.txt

# Print success message
echo "Build completed successfully!"
