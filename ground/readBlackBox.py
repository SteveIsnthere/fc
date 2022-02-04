import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

blackBox_path = os.path.join(os.path.expanduser('~'), "blackBox.csv")
# reading CSV file
data = pd.read_csv(blackBox_path)

# converting column data to list
time = np.array(data["time"].tolist())

pitch = np.array(data["pitch"].tolist())
roll = np.array(data["roll"].tolist())
heading = np.array(data["heading"].tolist())

aileronInput = np.array(data["aileronInput"].tolist())
elevatorInput = np.array(data["elevatorInput"].tolist())

Baro_altitude = np.array(data["Baro_altitude"].tolist())
Baro_vertical_speed = np.array(data["Baro_vertical_speed"].tolist())
Baro_temperature = np.array(data["Baro_temperature"].tolist())

GPS_locked = np.array(data["GPS_locked"].tolist())
index_locked = np.where(GPS_locked == 1)[0]
GPS_coord_x = np.array(data["GPS_coord_x"].tolist())
GPS_coord_y = np.array(data["GPS_coord_y"].tolist())
GPS_altitude = np.array(data["GPS_altitude"].tolist())
GPS_heading = np.array(data["GPS_heading"].tolist())
GPS_speed = np.array(data["GPS_speed"].tolist())
GPS_satellites = np.array(data["GPS_satellites"].tolist())

accceleration = np.array(data["accceleration"].tolist())/9.81

# 3d flight path
fig = plt.figure()
ax = fig.add_subplot(projection="3d")

def set_axes_equal(ax):
    '''Make axes of 3D plot have equal scale so that spheres appear as spheres,
    cubes as cubes, etc..  This is one possible solution to Matplotlib's
    ax.set_aspect('equal') and ax.axis('equal') not working for 3D.

    Input
      ax: a matplotlib axis, e.g., as output from plt.gca().
    '''

    x_limits = ax.get_xlim3d()
    y_limits = ax.get_ylim3d()
    z_limits = ax.get_zlim3d()

    x_range = abs(x_limits[1] - x_limits[0])
    x_middle = np.mean(x_limits)
    y_range = abs(y_limits[1] - y_limits[0])
    y_middle = np.mean(y_limits)
    z_range = abs(z_limits[1] - z_limits[0])
    z_middle = np.mean(z_limits)

    # The plot bounding box is a sphere in the sense of the infinity
    # norm, hence I call half the max range the plot radius.
    plot_radius = 0.5*max([x_range, y_range, z_range])

    ax.set_xlim3d([x_middle - plot_radius, x_middle + plot_radius])
    ax.set_ylim3d([y_middle - plot_radius, y_middle + plot_radius])
    ax.set_zlim3d([z_middle - plot_radius, z_middle + plot_radius])

ax.plot(
    GPS_coord_x[index_locked], GPS_coord_y[index_locked], Baro_altitude[index_locked]
)

ax.set_xlabel("X")
ax.set_ylabel("Y")
ax.set_zlabel("Z")
set_axes_equal(ax)
plt.show()

# detailed info
plt.subplot(3, 4, 1)
plt.title("pitch")
plt.ylim([-91, 91])
plt.plot(time, pitch)

plt.subplot(3, 4, 2)
plt.title("roll")
plt.ylim([-181, 181])
plt.plot(time, roll)

plt.subplot(3, 4, 3)
plt.title("aileronInput")
plt.ylim([-1.1, 1.1])
plt.plot(time, aileronInput)

plt.subplot(3, 4, 4)
plt.title("elevatorInput")
plt.ylim([-1.1, 1.1])
plt.plot(time, elevatorInput)

plt.subplot(3, 4, 5)
plt.axis('equal')
plt.title("postion")

# order_arr = np.array(list(range(len(GPS_coord_y[index_locked]))))
# color = 1/max(order_arr)*order_arr
# plt.scatter(GPS_coord_x[index_locked],GPS_coord_y[index_locked],c=color)
# plt.gray()
plt.plot(GPS_coord_x[index_locked], GPS_coord_y[index_locked])

plt.subplot(3, 4, 6)
plt.title("GPS_altitude")
plt.plot(time[index_locked], GPS_altitude[index_locked])

plt.subplot(3, 4, 7)
plt.title("GPS_speed")
plt.plot(time[index_locked], GPS_speed[index_locked])

plt.subplot(3, 4, 8)
plt.title("GPS_heading")
plt.plot(time[index_locked], GPS_heading[index_locked])

plt.subplot(3, 4, 9)
plt.title("Baro_altitude")
plt.scatter(time, Baro_altitude,s=1)

# plt.subplot(3, 4, 10)
# plt.title("Baro_vertical_speed")
# plt.plot(time, Baro_vertical_speed)
plt.subplot(3, 4, 10)
plt.title("Baro_vertical_speed")
plt.plot(time[1:], Baro_vertical_speed[1:])
plt.plot(time[1:], (Baro_altitude[1:]-Baro_altitude[:-1])/(time[1:]-time[:-1]))

plt.subplot(3, 4, 11)
plt.title("Baro_temperature")
plt.scatter(time, Baro_temperature,s=1)

plt.subplot(3, 4, 12)
plt.title("accceleration")
plt.scatter(time, accceleration,s=1)




plt.show()

plt.scatter(list(range(len(time)-1)),time[1:]-time[:-1],s=1)

plt.show()

print(np.mean(time[1:]-time[:-1]))