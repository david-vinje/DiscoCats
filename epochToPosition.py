from skyfield.api import load, wgs84

name = 'VIGORIDE 6'
stations_url = 'https://celestrak.org/NORAD/elements/gp.php?GROUP=active&FORMAT=tle'
satellites = load.tle_file(stations_url)
by_name = {sat.name: sat for sat in satellites}
satellite = by_name[name]

ts = load.timescale()
lines = [x.rstrip('\n') for x in open('epochs.txt', 'r').readlines()]
n = len(lines) - 1
first_line = lines[n]
positions_file = open('positions.txt', 'a')
    
latest_timestamp_file = open('latest_timestamp.txt', 'r')
latest_timestamp = latest_timestamp_file.readline()
latest_timestamp_file.close()

i = n
while lines[i] != latest_timestamp:
    i -= 1
    line = lines[i]
    time = lines[i].split(' ')
    year, month, day = [int(x) for x in time[0].split('-')]
    hour, minute, second = [int(x) for x in time[1].split(':')]
    time = ts.tt(year, month, day, hour, minute, second)
    pos = [str(x) for x in satellite.at(time).position.km]
    positions_file.write(' '.join(pos) + '\n')
positions_file.close()

latest_timestamp_file = open('latest_timestamp.txt', 'w')
latest_timestamp_file.write(first_line)
latest_timestamp_file.close()