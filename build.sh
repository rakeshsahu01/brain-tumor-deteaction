#!/bin/bash

# Exit on any error
set -e

echo "Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

echo "Installing and building React frontend..."
cd client
npm install
npm run build
cd ..

echo "Build completed successfully!"
