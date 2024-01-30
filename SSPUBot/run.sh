#!/bin/bash
Xvfb :7 -screen 0 1336x768x24 2>/dev/null &
export DISPLAY=:7
chmod a+rwx ./data -R
while true;
do
    python3 main.py onDocker
    sleep 10m
    pkill -9 firefox
    pkill -9 geckodriver
    pkill -9 firefox-bin
    sleep 35m
done
