#!/bin/bash
echo "[STARTING-SERVER] [PORT] 8000"

echo "Looking for asgi application..."
cd server

#STARTING APPLICATION
daphne core.asgi:application  --bind 0.0.0.0 &

cd ../
echo "Running Django Server [8000]"

