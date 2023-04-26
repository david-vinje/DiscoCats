#!/bin/bash

url="https://celestrak.org/NORAD/elements/gp.php?GROUP=active&FORMAT=tle"
data=$(curl -s $url)
echo ${data}
if ! (echo "$data" | grep -A 2 "VIGORIDE 6" | grep -qF -x -m 1 -f - discoTLEhistory.log); then
    vig_data=($(echo "$data" | grep -A 2 "VIGORIDE 6"))
    echo ${vig_data[0]}
    vig_list=(${vig_data[@]/$'\n'/}) # remove newlines from the array
    echo "${vig_list[0]}"
    echo "${vig_list[1]}"
    echo "${vig_list[2]}"
    echo "${vig_list}" >> discoTLEhistory.log
fi
