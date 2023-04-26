#Before running this code you will need to:
    #1. sudo apt install python3-pip 
    #2. pip install skyfield 
    #3. pip install matplotlib
    #4. pip install numpy
    #5. Can be run from terminal: python3 tleDectectionScript2.py STARLINK-5948 "1 55991U 23042F   23110.91667824 -.00017933  00000+0 -31878-3 0  9994" "2 55991  43.0018  31.0784 0001495 260.8786 317.1824 15.48926415  1301"

#Imports the EarthSatellite and load functions from the skyfield.api module. 
#EarthSatellite is a class that represents an Earth satellite and allows you to compute its position and velocity at a given time. 
#load is a function that loads a data file or URL and returns an object that can be used to create EarthSatellite objects.

# print(WGS84_RADIUS_EQUATORIAL.km)

from skyfield.api import EarthSatellite, load, wgs84
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
from datetime import time, datetime

print(wgs84.radius.km)

#TimeScale object using the load.timescale() function. 
#A TimeScale object represents a linear scale of time and allows you to create Time objects that can be used to represent specific dates and times. 
ts = load.timescale()

#TLE data for the satellite. TLE data consists of two lines of text that contain information about the satellite's orbit, such as its position and velocity.
name = 'VIGORIDE 6'
stations_url = 'https://celestrak.org/NORAD/elements/gp.php?GROUP=active&FORMAT=tle'
satellites = load.tle_file(stations_url)
by_name = {sat.name: sat for sat in satellites}
satellite = by_name[name]

# name_of_object = 'STARLINK-5948'
# line1 = '1 55991U 23042F   23110.91667824 -.00017933  00000+0 -31878-3 0  9994'
# line2 = '2 55991  43.0018  31.0784 0001495 260.8786 317.1824 15.48926415  1301'

#-----------------------------------------------------------------------------
    # Work-in-progress (Compare the time of TLE and the time of detection)
#-----------------------------------------------------------------------------
# TLE_year = line1[18:20]
# TLE_days = float(line1[20:33])
# epoch_in_date = datetime.datetime((2000 + int(TLE_year)), 1, 1) + datetime.timedelta(days=TLE_days)
# print('epoch_in_date', epoch_in_date)
#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------

# EarthSatellite object using the TLE data, the name of the satellite ("ISS (ZARYA)"), and the TimeScale object.
# sat = EarthSatellite(line1, line2, name_of_object, ts)
# create a Time object for the detection timestamp (e.g., April 19, 2023 at 12:00:00 UTC)
# detection_timestamp = ts.utc(2023, 4, 19, 12, 0, 0)
detection_timestamp = ts.now().tt_strftime()
print('detection_timestamp', detection_timestamp)
s = detection_timestamp.split(' ')
year, month, day = [int(x) for x in s[0].split('-')]
hour, minute, second = [int(x) for x in s[1].split(':')]
T = ts.tt(year, month, day, hour, minute, second)
detection_timestamp = T

# compute the position and velocity of the satellite at the detection timestamp
# computes the position and velocity of the satellite at the given Time object t using the EarthSatellite.at() method. 
#The .position and .velocity properties return the position and velocity vectors of the satellite, respectively. 
#These vectors are returned in units of kilometers and kilometers per second, respectively. 
#The values are assigned to the variables pos and vel using tuple unpacking
position = satellite.at(detection_timestamp).position
pos, vel = satellite.at(detection_timestamp).position.km, satellite.at(detection_timestamp).velocity.km_per_s
print(position)

# compute the latitude, longitude, and altitude of the satellite's subpoint at the detection timestamp
# computes the latitude, longitude, and altitude of the satellite's subpoint (i.e., the point on the Earth's surface directly below the satellite)...
# ... at the given Time object t using the EarthSatellite.at() method and the .subpoint() method. 
# The .latitude, .longitude, and .elevation properties return the latitude, longitude, and altitude values of the subpoint, respectively. 
#The .degrees method converts the latitude and longitude values from radians to degrees. 
#The values are assigned to the variables lat, lon, and alt using tuple unpacking.
lat, lon, alt = satellite.at(detection_timestamp).subpoint().latitude.degrees, satellite.at(detection_timestamp).subpoint().longitude.degrees, satellite.at(detection_timestamp).subpoint().elevation.km

# print the results
print("Info about " + name)
print("---------------------------------------")
print("From TLE the position and velocity was calcutated:")
print("Position: x={:.2f} km, y={:.2f} km, z={:.2f} km".format(pos[0], pos[1], pos[2]))
print("Velocity: vx={:.2f} km/s, vy={:.2f} km/s, vz={:.2f} km/s".format(vel[0], vel[1], vel[2]))
print("---------------------------------------")
print("From the position and velocity, the Lat, Lon, and Alt of the ISS at the time of the detection was calculated:")
print("Latitude: {:.2f} degrees".format(lat))
print("Longitude: {:.2f} degrees".format(lon))
print("Altitude: {:.2f} km".format(alt))
print("---------------------------------------")


#print("Position: x={:.2f} km, y={:.2f} km, z={:.2f} km".format(pos[0], pos[1], pos[2])): This line prints the position of the satellite in kilometers, with a precision of 2 decimal places for each coordinate (x, y, and z). The values of pos[0], pos[1], and pos[2] (which represent the x, y, and z coordinates of the position vector, respectively) are inserted into the string using the .format() method.
#print("Velocity: vx={:.2f} km/s, vy={:.2f} km/s, vz={:.2f} km/s".format(vel[0], vel[1], vel[2])): This line prints the velocity of the satellite in kilometers per second, with a precision of 2 decimal places for each coordinate (vx, vy, and vz). The values of vel[0], vel[1], and vel[2] (which represent the x, y, and z components of the velocity vector, respectively) are inserted into the string using the .format() method.
#print("Latitude: {:.2f} degrees".format(lat)): This line prints the latitude of the satellite in degrees, with a precision of 2 decimal places. The value of lat is inserted into the string using the .format() method.
#print("Longitude: {:.2f} degrees".format(lon)): This line prints the longitude of the satellite in degrees, with a precision of 2 decimal places. The value of lon is inserted into the string using the .format() method.
#print("Altitude: {:.2f} km".format(alt)): This line prints the altitude of the satellite in kilometers, with a precision of 2 decimal places. The value of alt is inserted into the string using the .format() method.

# Earth's radius in km
EARTH_RADIUS = wgs84.radius.km

# Convert lat, lon, and alt to x, y, and z coordinates
# phi = math.radians(90 - lat)
# theta = math.radians(lon)
# r = EARTH_RADIUS + alt
# x = r * math.sin(phi) * math.cos(theta)
# y = r * math.sin(phi) * math.sin(theta)
# z = r * math.cos(phi)
x, y, z = pos

# diffs = [abs(a-b) for a, b in [(x, x1), (y, y1), (z, z1)]]

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Plot Earth sphere
u, v = np.mgrid[0:2*np.pi:20j, 0:np.pi:10j]
a = EARTH_RADIUS*np.cos(u)*np.sin(v)
b = EARTH_RADIUS*np.sin(u)*np.sin(v)
c = EARTH_RADIUS*np.cos(v)
ax.plot_surface(a, b, c, cmap='Blues')

# Plot point at (x, y, z)
ax.scatter(x, y, z, c='r', marker='o')

# Set camera position and orientation
ax.view_init(elev=30, azim=-60)
ax.set_xlim([-2*EARTH_RADIUS, 2*EARTH_RADIUS])
ax.set_ylim([-2*EARTH_RADIUS, 2*EARTH_RADIUS])
ax.set_zlim([-2*EARTH_RADIUS, 2*EARTH_RADIUS])
ax.set_xlabel('X [km]')
ax.set_ylabel('Y [km]')
ax.set_zlabel('Z [km]')

plt.show()
