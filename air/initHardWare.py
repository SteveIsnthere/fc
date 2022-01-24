from kspInterface import *
from settings import *
#Barometer
barometer = KSP_baro()
baro_init_alt = ksp_altitude()
baro_init_temp = 15
#GPS
gps = KSP_gps()

#IMU
imu = KSP_imu()

#Pitot
pitot = KSP_Pitot()

#LORA
rfm9x = KSP_lora()

# Servo Control
def aileron_actuation(controlInput, trim):
    control_angle = controlInput*ailerons_actuation_range
    trim_angle = trim*ailerons_actuation_range
    output_angle = control_angle+trim_angle
    if output_angle > ailerons_actuation_limit:
        output_angle = ailerons_actuation_limit
    elif output_angle < -ailerons_actuation_limit:
        output_angle = -ailerons_actuation_limit
        
    ksp_set_roll(output_angle/ailerons_actuation_range)


def elevator_actuation(controlInput, trim):
    control_angle = controlInput*elevators_actuation_range
    trim_angle = trim*elevators_actuation_range
    output_angle = control_angle+trim_angle
    if output_angle > elevators_actuation_limit:
        output_angle = elevators_actuation_limit
    elif output_angle < -elevators_actuation_limit:
        output_angle = -elevators_actuation_limit

    ksp_set_pitch(output_angle/elevators_actuation_range)


def throttle_control(controlInput):
    output = controlInput*180
    if output > 180:
        output = 180
    elif output < 0:
        output = 0

    ksp_set_throttle(output/180)
