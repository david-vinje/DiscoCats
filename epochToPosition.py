from skyfield.api import load, wgs84

name = 'VIGORIDE 6'
stations_url = 'https://celestrak.org/NORAD/elements/gp.php?GROUP=active&FORMAT=tle'
satellites = load.tle_file(stations_url)
by_name = {sat.name: sat for sat in satellites}
satellite = by_name[name]

ts = load.timescale()
lines = open('epochs.txt', 'r').readlines()
file = open('positions.txt', 'a')

for line in lines:
    time = line.split(' ')
    year, month, day = [int(x) for x in time[0].split('-')]
    hour, minute, second = [int(x) for x in time[1].split(':')]
    time = ts.tt(year, month, day, hour, minute, second)
    pos, vel = satellite.at(time).position.km, satellite.at(time).velocity.km_per_s
    file.write(''.join((str(pos), str(vel))) + '\n')

file.close()