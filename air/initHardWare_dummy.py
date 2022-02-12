from settings import *
import board
import busio
from digitalio import DigitalInOut, Direction, Pull
from adafruit_servokit import ServoKit
import adafruit_rfm9x
ksp_mode = False
# LORA
# Configure LoRa Radio
CS = DigitalInOut(board.CE1)
RESET = DigitalInOut(board.D25)
spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)
rfm9x = adafruit_rfm9x.RFM9x(spi, CS, RESET, float(radio_frequency))
rfm9x.tx_power = 23

class Dummy_baro:
    @property
    def altitude(self):
        return 0
    @property
    def temperature(self):
        return 0

class Dummy_gps:
    @property
    def latitude(self):
        return 0
    @property
    def longitude(self):
        return 0
    @property
    def has_3d_fix(self):
        return True
    @property
    def satellites(self):
        return 15
    @property
    def altitude_m(self):
        return 0
    @property
    def speed_knots(self):
        return 0
    @property
    def track_angle_deg(self):
        #need further implemetation
        return 0

    def update(self):
        return

class Dummy_imu:
    @property
    def euler(self):
        return [0,0,0]
    @property
    def gyro(self):
        return [0,0,0]
    @property
    def linear_acceleration(self):
        return [0,0,0]
    @property
    def acceleration(self):
        return [9.81,0,0]

class Dummy_Pitot:
    @property
    def temperature(self):
        return 1
    @property
    def pressure(self):
        return 13

#Barometer
barometer = Dummy_baro()
baro_init_alt = 15
baro_init_temp = 15
#GPS
gps = Dummy_gps()

#IMU
imu = Dummy_imu()

#Pitot
pitot = Dummy_Pitot()

# Servo HAT
kit = ServoKit(channels=16)
kit.servo[0].angle = 0

# Servo Control
def aileron_actuation(controlInput, trim):
    control_angle = controlInput * ailerons_actuation_range
    trim_angle = trim * ailerons_actuation_range
    output_angle = control_angle + trim_angle
    if output_angle > ailerons_actuation_limit:
        output_angle = ailerons_actuation_limit
    elif output_angle < -ailerons_actuation_limit:
        output_angle = -ailerons_actuation_limit

    kit.servo[1].angle = -output_angle + ailerons_mid_point


def elevator_actuation(controlInput, trim):
    control_angle = controlInput * elevators_actuation_range
    trim_angle = trim * elevators_actuation_range
    output_angle = control_angle + trim_angle
    if output_angle > elevators_actuation_limit:
        output_angle = elevators_actuation_limit
    elif output_angle < -elevators_actuation_limit:
        output_angle = -elevators_actuation_limit

    kit.servo[14].angle = output_angle + elevators_mid_point
    kit.servo[15].angle = -output_angle + elevators_mid_point


def throttle_control(controlInput):
    output = controlInput * 180
    if output > 180:
        output = 180
    elif output < 0:
        output = 0
    kit.servo[0].angle = output
