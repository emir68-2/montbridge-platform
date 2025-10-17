#!/bin/bash

# Private Equity Due Diligence Platform - Backend Startup Script

echo "🚀 Starting Private Equity Due Diligence Platform Backend..."

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

# Check if pip is installed
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 is not installed. Please install pip."
    exit 1
fi

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📚 Installing Python dependencies..."
pip install -r requirements.txt

# Download spaCy model if not already installed
echo "🧠 Installing spaCy language model..."
python -m spacy download en_core_web_sm

# Create uploads directory if it doesn't exist
if [ ! -d "uploads" ]; then
    echo "📁 Creating uploads directory..."
    mkdir uploads
fi

# Start the Flask server
echo "🌟 Starting Flask server on http://localhost:5000"
echo "📊 Backend API will be available at http://localhost:5000/api"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

python app.py
