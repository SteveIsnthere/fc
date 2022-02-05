import os
radio_path = os.path.join(os.path.expanduser('~'), "dummyRadio.txt")
reciver_path = os.path.join(os.path.expanduser('~'), "dummyReciver.txt")
reciver = open(reciver_path, "r")
import time

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

    print(content)
    f = open(radio_path, "w")
    f.write(content)
    f.close()


def reciveTelemetry():
    telemetry = None

    telemetry = reciver.readline().split(",")
    return telemetry
