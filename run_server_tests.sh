#!/bin/bash

error="\e[1;31m[ERROR]\e[0m"
execution="\e[0;36m[INFO]\e[0m"

echo -e "$execution [...]"



#START SERVER
. ./run_server.sh

echo "$execution [SERVER-BOOT-COMPLETE]"
#Find tests
sleep 10s
cd server
var=$(python3 test_runner.py | grep "Failing Tests" -c)

if [ $var = 0 ];
then
    echo "$execution [All tests pass]"
else
    echo "$error All clean!"
    exit -1
fi


echo "$execution Claning up!"