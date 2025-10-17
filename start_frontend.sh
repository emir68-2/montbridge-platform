#!/bin/bash

# Private Equity Due Diligence Platform - Frontend Startup Script

echo "🚀 Starting Private Equity Due Diligence Platform Frontend..."

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install Node.js 16 or higher."
    exit 1
fi

# Check if npm is installed
if ! command -v npm &> /dev/null; then
    echo "❌ npm is not installed. Please install npm."
    exit 1
fi

# Navigate to frontend directory
cd src-frontend

# Check if package.json exists
if [ ! -f "package.json" ]; then
    echo "❌ package.json not found in src-frontend directory."
    exit 1
fi

# Install dependencies if node_modules doesn't exist
if [ ! -d "node_modules" ]; then
    echo "📚 Installing frontend dependencies..."
    npm install
fi

# Start the React development server
echo "🌟 Starting React development server on http://localhost:3000"
echo "🌐 Frontend will be available at http://localhost:3000"
echo ""
echo "Make sure the backend server is running on http://localhost:5000"
echo "Press Ctrl+C to stop the server"
echo ""

npm start
