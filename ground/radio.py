import serial
import time
import numpy as np
import base64
ser = serial.Serial('/dev/cu.usbmodem101',baudrate=115200)

def getValues():
    data = b"3456789123456789123456789123456789123456789\n"
    print(len(data))
    ser.write(data)
    arduinoData = ser.readline().decode("ascii")
    
    return len(arduinoData)


while(1):

    userInput = input('Get data point?')
    if userInput == 'y':
        print(getValues())
