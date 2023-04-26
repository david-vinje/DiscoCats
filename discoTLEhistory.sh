#!/bin/bash

url="https://celestrak.org/NORAD/elements/gp.php?GROUP=active&FORMAT=tle"
data=$(curl -s $url)
if ! (echo "$data" | grep -A 2 "VIGORIDE 6" | grep -qF -x -m 1 -f - discoTLEhistory.log); then
    echo "$data" | grep -A 2 "VIGORIDE 6" >> discoTLEhistory.log
fi
