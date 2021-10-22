#!/bin/bash

error="\e[1;31m[ERROR]\e[0m"
execution="\e[0;36m[INFO]\e[0m"

echo "$execution ssh into remote server"


echo "$execution Kill uvicorn workers"
fuser -k 8000/tcp

echo "$execution Starting deployment"
git pull --rebase origin master

pm2 restart 0
pm2 save

echo "$execution Deployed"
