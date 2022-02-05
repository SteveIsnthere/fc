from redis import Redis
shared = Redis('localhost')

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
    shared.set('ground',content)


def reciveTelemetry():
    telemetry_ = shared.get('air')
    if telemetry_ != "":
        telemetry = telemetry_.split(",")
        return telemetry
