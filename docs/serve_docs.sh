#!/bin/bash
# Setup and serve documentation locally

echo "Setting up documentation environment..."

# Install documentation dependencies
pip install -r requirements.txt

# Build the documentation
echo "Building documentation..."
make clean-build

# Serve the documentation
echo "Starting documentation server..."
echo "Open your browser to: http://localhost:8000"
make serve
