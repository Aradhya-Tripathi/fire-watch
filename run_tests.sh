#!/bin/bash

echo "[STARTING TESTS]"

#START SERVER
. ./run_server.sh

echo "[SERVER-BOOT-COMPLETE]"
#Find tests
sleep 10s
cd server/tests
python3 -m unittest test_server.py
python3 -m unittest test_units.py

echo "[STOPPING AND CLEANING UP]"