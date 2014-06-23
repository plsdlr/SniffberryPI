#!/bin/bash


su root -c "airmon-ng start wlan0"
sleep 3
su root -c "python /home/pi/SniffberryPI.py"
sleep 3
su pi -c "jackd -P 95 -p 32 -d dummy -C 1 &"
sleep 3
su pi -c "alsa_out -d hw:1 2>&1 > /dev/null &"
sleep 1
su pi -c "sclang /home/pi/test.scd"


