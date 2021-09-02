#!/bin/bash
echo "[STARTING-SERVER] [PORT] 8000"

echo "Looking for wsgi application..."
cd server

#STARTING APPLICATION
gunicorn core.wsgi --reload --bind 0.0.0.0:8000 &

cd ../
echo "Running Django Server [8000]"

