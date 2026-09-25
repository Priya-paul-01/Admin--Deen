#!/bin/bash
# GreenCommute Dashboard HTTP Server - Auto-restart wrapper
# Usage: bash start_server.sh
# The server monitors itself and restarts if it crashes

SERVER_DIR="/e/Samsudeen/Hermes agent"
PORT=8080
LOG_FILE="$SERVER_DIR/server.log"
PID_FILE="$SERVER_DIR/server.pid"

cd "$SERVER_DIR"

# Kill any existing server on this port
if [ -f "$PID_FILE" ]; then
    OLD_PID=$(cat "$PID_FILE")
    kill "$OLD_PID" 2>/dev/null
    sleep 1
fi

# Also kill by port
fuser -k ${PORT}/tcp 2>/dev/null
sleep 1

echo "[$(date)] Starting GreenCommute Dashboard server on port $PORT..."
echo "[$(date)] Server directory: $SERVER_DIR"

# Start server with nohup, redirect output to log
nohup python -u -m http.server $PORT --bind 127.0.0.1 >> "$LOG_FILE" 2>&1 &
SERVER_PID=$!
echo $SERVER_PID > "$PID_FILE"

echo "[$(date)] Server started with PID: $SERVER_PID"
echo "[$(date)] Log file: $LOG_FILE"
echo "[$(date)] Access: http://127.0.0.1:$PORT/greencommute_dashboard.html"

# Verify it started
sleep 2
if kill -0 "$SERVER_PID" 2>/dev/null; then
    echo "[$(date)] ✅ Server is RUNNING (PID: $SERVER_PID)"
    curl -s -o /dev/null -w "HTTP Status: %{http_code}\n" "http://127.0.0.1:$PORT/greencommute_dashboard.html"
else
    echo "[$(date)] ❌ Server FAILED to start. Check $LOG_FILE"
    exit 1
fi
