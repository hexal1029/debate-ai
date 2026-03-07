#!/bin/bash
# Script to start the Next.js frontend server

echo "=========================================="
echo "Starting AI Debate Frontend Server"
echo "=========================================="

cd "$(dirname "$0")/frontend"

# Check if node_modules exists
if [ ! -d "node_modules" ]; then
    echo "❌ node_modules not found!"
    echo "Installing dependencies..."
    npm install
    echo "✓ Dependencies installed"
fi

# Check if .env.local exists
if [ ! -f ".env.local" ]; then
    echo "⚠️  .env.local not found, using defaults"
fi

echo ""
echo "✓ Dependencies ready"
echo ""
echo "Starting server on http://localhost:3000"
echo "Press Ctrl+C to stop"
echo ""
echo "=========================================="

# Start the development server
npm run dev
