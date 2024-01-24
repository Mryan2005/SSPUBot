#!/bin/bash
chmod a+rwx ./data -R
while true;
do
    python3 main.py onDocker
    sleep 30m
done
