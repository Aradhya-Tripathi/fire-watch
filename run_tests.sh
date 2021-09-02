#!/bin/bash

echo "[STARTING TESTS]"

#START SERVER
. ./run_server.sh

echo "[SERVER-BOOT-COMPLETE]"
#Find tests
sleep 10s
cd server/tests
python3 -m unittest test_server.py

echo "[STOPPING AND CLEANING UP]"
fuser -k 8000/tcp