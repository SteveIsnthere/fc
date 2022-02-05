import serial
import time
radio = serial.Serial('/dev/cu.usbmodem101', baudrate=115200)

last_sent_data = time.time()
min_sentData_interval = 1/60

def sendData(content):
    global last_sent_data
    current_time = time.time()
    since_last_sent = current_time-last_sent_data
    if since_last_sent>min_sentData_interval:
        last_sent_data = current_time
    else:
        return
    
    try:
        print(content)
        package = content.encode("ascii")
        #radio.write(package)
    except:
        pass

def reciveTelemetry():
    telemetry = None
    try:
        telemetry = radio.readline().decode("ascii").split(",")
        return telemetry
    except:
        print("reciveTelemetry() Error")