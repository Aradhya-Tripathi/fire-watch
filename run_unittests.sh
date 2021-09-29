#!/bin/bash

error="\e[1;31m[ERROR]\e[0m"
execution="\e[0;36m[INFO]\e[0m"

echo -e "$execution [...]"


echo "$execution [STARTING TESTS]"

cd servettest

r/authentication
python3 -m unicd ../..

echo "$execution Claning up!"