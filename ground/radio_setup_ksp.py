from redis import Redis
shared = Redis('localhost')

import time

last_sent_data = time.monotonic()
last_recived_data = time.monotonic()
min_dataExchange_interval = 1/30

def sendData(content):
    global last_sent_data
    current_time = time.monotonic()
    since_last_sent = current_time-last_sent_data
    if since_last_sent>min_dataExchange_interval:
        last_sent_data = current_time
    else:
        return

    shared.set('ground',content)


def reciveTelemetry():
    global last_recived_data
    current_time = time.monotonic()
    since_last_sent = current_time-last_recived_data
    if since_last_sent>min_dataExchange_interval:
        last_recived_data = current_time
    else:
        return None
    telemetry_raw = shared.get('air')
    if telemetry_raw is None:        
        return None
    telemetry = telemetry_raw.decode("ascii")
    if telemetry == "":
        return None
    telemetry=telemetry.split(",")
    return telemetry