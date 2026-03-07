#!/bin/bash
# Script to start the FastAPI backend server

echo "=========================================="
echo "Starting AI Debate Backend Server"
echo "=========================================="

cd "$(dirname "$0")/backend"

# Check if venv exists
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found!"
    echo "Creating virtual environment..."
    python3 -m venv venv
    echo "✓ Virtual environment created"

    echo "Installing dependencies..."
    source venv/bin/activate
    pip install -r requirements.txt
    echo "✓ Dependencies installed"
fi

# Activate virtual environment
source venv/bin/activate

# Check if .env exists
if [ ! -f ".env" ]; then
    echo "❌ .env file not found!"
    echo "Please create .env file with your ANTHROPIC_API_KEY"
    exit 1
fi

echo ""
echo "✓ Virtual environment activated"
echo "✓ Environment variables loaded"
echo ""
echo "Starting server on http://localhost:8000"
echo "Press Ctrl+C to stop"
echo ""
echo "=========================================="

# Start the server
uvicorn main:app --reload --host 0.0.0.0 --port 8000
