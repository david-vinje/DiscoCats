from skyfield.api import load, EarthSatellite
from datetime import datetime, timedelta
from sys import float_info

name = 'VIGORIDE 6'
stations_url = 'https://celestrak.org/NORAD/elements/gp.php?GROUP=active&FORMAT=tle'
satellites = load.tle_file(stations_url)
by_name = {sat.name: sat for sat in satellites}
satellite = by_name[name]

ts = load.timescale()
detections_epochs = [x.rstrip('\n') for x in open('epochs.txt', 'r').readlines()]
n = len(detections_epochs) - 1
newest_epoch = detections_epochs[n]
positions_file = open('positions.txt', 'a')
    
latest_timestamp_file = open('latest_timestamp.txt', 'r')
latest_timestamp = latest_timestamp_file.readline()
latest_timestamp =  '0000-00-00 00:00:00 TT' if latest_timestamp == '' else latest_timestamp
latest_timestamp_file.close()

def tle_to_datetime(tle):
    TLE_year = tle[18:20]
    TLE_days = float(tle[20:33])
    return datetime((2000 + int(TLE_year)), 1, 1) + timedelta(days=TLE_days)

def find_closest_tle(detection_timestamp):
    lines = open('discoTLEhistory.log').readlines()
    i = len(lines) - 2
    diff = float('inf')
    m = float_info.max
    while True:
        line = lines[i]
        tle_timestamp = tle_to_datetime(line)
        tmp = abs(detection_timestamp - tle_timestamp).total_seconds()
        if tmp > diff:
            diff = tmp
            break
        i -= 3
        diff = tmp
    line1 = lines[i]
    line2 = lines[i+1]
    satellite = EarthSatellite(line1, line2, name, ts)
    return satellite

tle_timestamp_dictionary = open('detections_with_tle.txt', 'a')

i = n
detection_epoch = detections_epochs[i]
while detection_epoch != latest_timestamp:
    i -= 1
    date, time, _ = detection_epoch.split(' ')
    year, month, day = [int(x) for x in date.split('-')]
    hour, minute, second = [int(x) for x in time.split(':')]
    detection_timestamp = datetime(year, month, day, hour, minute, second)
    satellite = find_closest_tle(detection_timestamp)
    s = ','.join([str(detection_timestamp), str(satellite)]) + '\n'
    tle_timestamp_dictionary.write(s)
    terrestial_time = ts.tt(year, month, day, hour, minute, second)
    pos = [str(x) for x in satellite.at(terrestial_time).position.km]
    positions_file.write(' '.join(pos) + '\n')
    detection_epoch = detections_epochs[i]

positions_file.close()
tle_timestamp_dictionary.close()

latest_timestamp_file = open('latest_timestamp.txt', 'w')
latest_timestamp_file.write(newest_epoch)
latest_timestamp_file.close()