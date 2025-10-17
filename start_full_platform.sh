#!/bin/bash

echo "🚀 Starting PE Due Diligence Platform - Full Version"
echo "=================================================="

# Check if backend is running
if curl -s http://localhost:5001/api/health > /dev/null; then
    echo "✅ Backend is already running on http://localhost:5001"
else
    echo "🔧 Starting backend server..."
    cd "/Users/emir/cursor practice"
    source venv/bin/activate
    python app.py &
    sleep 3
    echo "✅ Backend started on http://localhost:5001"
fi

# Check if frontend is running
if curl -s http://localhost:3000 > /dev/null; then
    echo "✅ Frontend is already running on http://localhost:3000"
else
    echo "🔧 Starting frontend server..."
    cd "/Users/emir/cursor practice/src-frontend"
    npm start &
    sleep 8
    echo "✅ Frontend started on http://localhost:3000"
fi

echo ""
echo "🌟 Platform Status:"
echo "   Backend API:  http://localhost:5001/api"
echo "   Frontend UI:  http://localhost:3000"
echo "   Demo Page:    file:///Users/emir/cursor practice/demo.html"
echo ""
echo "📱 Opening browser..."
open http://localhost:3000

echo "🎉 PE Due Diligence Platform is ready!"
echo "   Navigate through the professional dashboard to explore:"
echo "   • Dashboard - Overview and key metrics"
echo "   • Upload & Process - File upload and analysis"
echo "   • Valuation Analysis - DCF, Comps, Precedent methods"
echo "   • Risk Assessment - Due diligence and risk analysis"
