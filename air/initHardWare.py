from settings import *
ksp_mode = False
# I2C setup
import board
import adafruit_bmp3xx
import adafruit_gps
import adafruit_bno055
import adafruit_lps35hw
import adafruit_rfm9x
import busio
from digitalio import DigitalInOut, Direction, Pull
from adafruit_servokit import ServoKit
i2c = board.I2C()  # uses board.SCL and board.SDA

# Barometer
barometer = adafruit_bmp3xx.BMP3XX_I2C(i2c)
barometer.pressure_oversampling = 4
barometer.temperature_oversampling = 4
baro_init_alt = None
while baro_init_alt is None:
    baro_init_alt = barometer.altitude
baro_init_temp = None
while baro_init_temp is None:
    baro_init_temp = barometer.temperature

# GPS
gps = adafruit_gps.GPS_GtopI2C(i2c, debug=False)
gps.send_command(b"PMTK314,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0")
gps.send_command(b"PMTK220,200")

# IMU
imu = adafruit_bno055.BNO055_I2C(i2c)

# Pitot
pitot = adafruit_lps35hw.LPS35HW(i2c)

# LORA
# Configure LoRa Radio
CS = DigitalInOut(board.CE1)
RESET = DigitalInOut(board.D25)
spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)
rfm9x = adafruit_rfm9x.RFM9x(spi, CS, RESET, float(radio_frequency))
rfm9x.tx_power = 23

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
