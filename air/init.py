from initHardWare import *
import os
import numpy as np
import time
from multiprocessing import Value

# init parameters
readyToArm = Value("i", 0)
readyToFly = Value("i", 0)  # Armed

current_X = Value("f", 0)
current_Y = Value("f", 0)
current_Heading = Value("f", 0)

init_x = Value("f", 0)
init_y = Value("f", 0)
init_imu_heading = Value("f", 0)
init_gps_altitude = Value("f", 0)

touch_down_x = Value("f", 0)
touch_down_y = Value("f", 0)

# level0 Controller
# telemetry
shared_pitch = Value("f", 0)
shared_roll = Value("f", 0)
shared_imu_heading = Value("f", 0)
shared_raw_aileron_input = Value("f", 0)
shared_raw_elevator_input = Value("f", 0)
shared_accceleration = Value("f", 0)
# commands
desired_pitch = Value("f", 20)
desired_roll = Value("f", -5)
aileronTrim = Value("f", aileronTrim)
elevatorTrim = Value("f", elevatorTrim)

# higherlevelController
desired_vs = Value("f", 0)
desired_heading = Value("f", 0)
desired_throttle = Value("f", 0)
manual_throttle_unlocked = Value("i", 0)
calibrate_heading = Value("i", 0)
imu_heading_compensation = Value("f", 0)
# flight modes
flight_mode = Value("i", 1)
# 0:full manual
manual_throttle_input = Value("f", 0)
# 1:fly by wire (partial manual)
manual_roll_change_per_sec = Value("f", 0)
manual_pitch_change_per_sec = Value("f", 0)
# 2 :1.Circle(3)
circle_altitude = Value("f", 0)
circle_bankAngle = Value("f", 20)

# sensors
# Barometer & Pitot
Baro_altitude = Value("f", baro_init_alt)
Baro_vertical_speed = Value("f", 0)
last_Baro_altitude = baro_init_alt
last_Baro_vertical_speed = 0
Baro_temperature = Value("f", baro_init_temp)
last_Baro_temperature = baro_init_temp

Pitot_pressure = Value("f", 0)
Pitot_temperature = Value("f", 0)


def Pitot_air_speed():
    return


# GPS
GPS_locked = Value("i", 0)
GPS_latitude = Value("f", 0)
GPS_longitude = Value("f", 0)
GPS_altitude = Value("f", 0)
GPS_speed = Value("f", 0)
GPS_heading = Value("f", 0)
GPS_satellites = Value("i", 0)

GPS_coord_x = Value("f", 0)
GPS_coord_y = Value("f", 0)

# Radio
telemetry_mode = 2
last_received_upLink = time.time()
since_last_received_upLink = Value("f", 0)
calibrate_heading = Value("i", 0)

# BlackBox
blackBox_path = os.path.join(os.path.expanduser('~'), "blackBox.csv")

# System General setup
start_up_time = time.time()
control_loop_interval = 1 / control_loop_freq
secondary_loop_interval = 1 / secondary_loop_freq

max_acceleration = max_g_force * 9.81

'''
(readyToArm, readyToFly, current_X, current_Y, current_Heading, init_x, init_y, init_imu_heading, init_gps_altitude,touch_down_x,
 touch_down_y, shared_pitch, shared_roll, shared_imu_heading, shared_raw_aileron_input,
 shared_raw_elevator_input, shared_accceleration, desired_pitch, desired_roll, aileronTrim, elevatorTrim,
 desired_vs, desired_heading, desired_throttle, manual_throttle_unlocked, calibrate_heading,imu_heading_compensation,flight_mode, manual_throttle_input,
  manual_roll_change_per_sec, manual_pitch_change_per_sec, circle_altitude, circle_bankAngle,
 Baro_altitude, Baro_vertical_speed, last_Baro_altitude, last_Baro_vertical_speed, Baro_temperature, last_Baro_temperature,
 Pitot_pressure, Pitot_temperature, GPS_locked, GPS_latitude, GPS_longitude, GPS_altitude, GPS_speed, GPS_heading, GPS_satellites,
 GPS_coord_x, GPS_coord_y, telemetry_mode, last_received_upLink, since_last_received_upLink, calibrate_heading, blackBox_path,
 start_up_time, control_loop_interval, secondary_loop_interval, max_acceleration)
'''


def controlInputRequired(current, current_v, target, timeToAlign, maxAuthority):
    # maxAuthority in acceleration
    diff = target - current
    accelerationNeeded = 2 * (diff / timeToAlign **
                              2 - current_v / timeToAlign)
    controlInput = accelerationNeeded / maxAuthority
    # if controlInput >= 1:
    #     controlInput = 1
    # elif controlInput <= -1:
    #     controlInput = -1
    return controlInput

def resonable_mean(raw_data_list):
    raw_data_list.remove(max(raw_data_list))
    raw_data_list.remove(max(raw_data_list))
    raw_data_list.remove(min(raw_data_list))
    raw_data_list.remove(min(raw_data_list))
    return sum(raw_data_list) / len(raw_data_list)
