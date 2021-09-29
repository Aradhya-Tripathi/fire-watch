#!/bin/bash

error="\e[1;31m[ERROR]\e[0m"
execution="\e[0;36m[INFO]\e[0m"

echo -e "$execution [...]"


echo "$execution [STARTING TESTS]"

cd server/authentication
python3 -m unittest

cd ../..

echo "$execution Claning up!"