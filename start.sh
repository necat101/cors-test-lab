#!/bin/bash
cd "$(dirname "$0")"
echo "Starting CORS Test Lab..."
python3 server/api_server.py &
API_PID=$!
sleep 1
python3 client/server.py &
CLIENT_PID=$!
echo ""
echo "✅ Running!"
echo "   http://localhost:8000"
echo "   http://localhost:8001"
echo ""
echo "Press Ctrl+C to stop"
trap "kill $API_PID $CLIENT_PID 2>/dev/null; exit 0" INT
wait
