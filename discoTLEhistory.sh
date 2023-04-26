#!/bin/bash

url="https://celestrak.org/NORAD/elements/gp.php?GROUP=active&FORMAT=tle"
data=$(curl -s $url)
#echo "$data" | grep -A 2 "VIGORIDE 6" | tail -2 >> discoTLEhistory.log
if ! (echo "$data" | grep -A 2 "VIGORIDE 6" | tail -2 | grep -qF -x -f - discoTLEhistory.log); then
    echo "$data" | grep -A 2 "VIGORIDE 6" >> discoTLEhistory.log
fi
