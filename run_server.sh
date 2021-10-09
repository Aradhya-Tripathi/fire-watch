#!/bin/bash

error="\e[1;31m[ERROR]\e[0m"
execution="\e[0;36m[INFO]\e[0m"

echo -e "$execution [...]"


echo "$execution [STARTING-SERVER] [PORT] 8000"

echo "$execution Looking for asgi application..."
cd server

# STARTING APPLICATION
uvicorn core.asgi:application  --port 8000 --reload &

cd ../
echo "$execution Running Django Server [8000]"

