#!/bin/bash

error="\e[1;31m[ERROR]\e[0m"
execution="\e[0;36m[INFO]\e[0m"

echo -e "$execution [...]"



# START SERVER
if [ $1 -eq "0" ];
then
    . ./run_server.sh
    echo "$execution [SERVER-BOOT-COMPLETE]"
fi

# Find tests
sleep 5s
cd server

echo "$execution Entered: $1"

if [ $1 -eq "1" ];
then
    echo "$execution Running Unit Tests"
    var=$(python3 test_runner.py --unit-tests 1 | grep "Failing Tests" -c)

else
    echo "$error No unit tests ran"
    var=$(python3 test_runner.py --unit-tests 0| grep "Failing Tests" -c)

fi

if [ $var = 0 ];
then
    echo "$execution All tests pass!"
else
    echo "$error Failing Tests!"
    cd ../
    exit -1
fi

if [ $2 = "shutdown" ];
then
    echo "$execution Killing port [...]"
    fuser -k 8000/tcp
fi

cd ../

echo "$execution Claning up!"