#!/bin/bash
echo "[STARTING-SERVER] [PORT] 8000"

echo "Looking for asgi application..."
cd server

#STARTING APPLICATION
uvicorn core.asgi:application  --port 8000 --reload &

cd ../
echo "Running Django Server [8000]"

