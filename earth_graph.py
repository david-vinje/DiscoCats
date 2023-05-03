import numpy as np
from skyfield.api import wgs84
from matplotlib import pyplot as plt

EARTH_RADIUS = wgs84.radius.km

lines = open('positions.txt').readlines()
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Plot Earth sphere
u, v = np.mgrid[0:2*np.pi:20j, 0:np.pi:10j]
a = EARTH_RADIUS*np.cos(u)*np.sin(v)
b = EARTH_RADIUS*np.sin(u)*np.sin(v)
c = EARTH_RADIUS*np.cos(v)
ax.plot_surface(a, b, c, cmap='Blues')

xs, ys, zs = [], [], []

for line in lines:
    x, y, z = [float(x) for x in line.split(' ')]
    xs.append(x)
    ys.append(y)
    zs.append(z)

# Plot point at (x, y, z)
ax.scatter(xs, ys, zs, c='r', marker='o')

# Set camera position and orientation
ax.view_init(elev=30, azim=-60)
ax.set_xlim([-2*EARTH_RADIUS, 2*EARTH_RADIUS])
ax.set_ylim([-2*EARTH_RADIUS, 2*EARTH_RADIUS])
ax.set_zlim([-2*EARTH_RADIUS, 2*EARTH_RADIUS])
ax.set_xlabel('X [km]')
ax.set_ylabel('Y [km]')
ax.set_zlabel('Z [km]')

plt.show()