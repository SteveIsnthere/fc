from settings import *
from initHardWare import *
import utm
import time
from multiprocessing import Value

control_loop_interval = round(1000 / control_loop_freq)  # in ms

# shared params
control_loop_interval = 1 / control_loop_freq
secondary_loop_interval = 1 / secondary_loop_freq

readyToArm = Value("i", 0)
readyToFly = Value("i", 0)
manual_throttle_unlocked = Value("i", 0)
start_up_time = time.time()

# level0 Controller
# telemetry
shared_pitch = Value("f", 0)
shared_roll = Value("f", 0)
shared_imu_heading = Value("f", 0)
shared_raw_aileron_input = Value("f", 0)
shared_raw_elevator_input = Value("f", 0)
# commands
desired_pitch = Value("f", 0)
desired_roll = Value("f", 0)
aileronTrim = Value("f", aileronTrim)
elevatorTrim = Value("f", elevatorTrim)


# higherlevelController
desired_vs = Value("f", 0)
desired_heading = Value("f", 0)
desired_throttle = Value("f", 0)
# flight modes
flight_mode = Value("i", 1)
# 0:full manual
manual_throttle_input = Value("f", 0)
manual_control_update_freq = Value("i", manual_control_update_freq)
# 1:fly by wire (partial manual)
manual_roll_change_per_sec = Value("f", 0)
manual_pitch_change_per_sec = Value("f", 0)
# 2 :1.Circle(3)
circle_altitude = Value("f", 0)


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


def utm_coords():
    utm_x, utm_y = utm.from_latlon(GPS_latitude, GPS_longitude)
    return [utm_x, utm_y]


# init parameters
x = 0
y = 0
flying_direction = 0

init_x = None
init_y = None
init_heading = None

touch_down_x = None
touch_down_y = None

mode = None

# Radio
telemetry_mode = 2
last_received_upLink = time.time()
since_last_received_upLink = Value("f", 0)
calibrate_heading = Value("i", 0)

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


# Servo Control
def aileron_actuation(controlInput, trim):
    control_angle = controlInput*ailerons_actuation_range
    trim_angle = trim*ailerons_actuation_range
    output_angle = control_angle+trim_angle
    if output_angle > ailerons_actuation_limit:
        output_angle = ailerons_actuation_limit
    elif output_angle < -ailerons_actuation_limit:
        output_angle = -ailerons_actuation_limit

    kit.servo[1].angle = -output_angle+ailerons_mid_point


def elevator_actuation(controlInput, trim):
    control_angle = controlInput*elevators_actuation_range
    trim_angle = trim*elevators_actuation_range
    output_angle = control_angle+trim_angle
    if output_angle > elevators_actuation_limit:
        output_angle = elevators_actuation_limit
    elif output_angle < -elevators_actuation_limit:
        output_angle = -elevators_actuation_limit

    kit.servo[14].angle = output_angle+elevators_mid_point
    kit.servo[15].angle = -output_angle+elevators_mid_point


def throttle_control(controlInput):
    output = controlInput*180
    if output > 180:
        output = 180
    elif output < 0:
        output = 0
    kit.servo[0].angle = output
