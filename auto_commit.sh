#!/bin/bash

while true; do
    git pull
    git add .
    git commit -m "auto commit"
    git push
    echo "Push done. Sleeping 10 minutes."
    sleep 600
done