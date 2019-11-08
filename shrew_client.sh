#!/bin/bash 

echo running iperf-client

#TODO: add your code

while true; do
	iperf -c "$1" -u -b 10M -t 0.4 &
	sleep 1.354
done
