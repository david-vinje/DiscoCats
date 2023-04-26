from skyfield.api import load

stations_url = 'https://celestrak.org/NORAD/elements/gp.php?GROUP=active&FORMAT=tle'
satellites = load.tle_file(stations_url)
by_name = {sat.name: sat for sat in satellites}
satellite = by_name['VIGORIDE 6']
tle_file = open('tles.txt', 'a')
tle_file.write(satellite)
tle_file.close()