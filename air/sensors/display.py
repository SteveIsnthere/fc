import busio
from digitalio import DigitalInOut, Direction, Pull
import board
# Import the SSD1306 module.
import adafruit_ssd1306

# Create the I2C interface.
i2c = busio.I2C(board.SCL, board.SDA)

# 128x32 OLED Display
reset_pin = DigitalInOut(board.D4)
display = adafruit_ssd1306.SSD1306_I2C(128, 32, i2c, reset=reset_pin)
# Clear the display.
display.fill(0)
display.show()
width = display.width
height = display.height


def showOnDisplay(content):
    display.fill(0)
    try:
        display.text(content, 0, 0, 1)
    except RuntimeError as error:
        print('Display Error: ', error)
    display.show()
    
showOnDisplay("")