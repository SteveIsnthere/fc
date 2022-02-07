from init import *
import csv

while True:
    gamepadInput = gamepad.read(64)
    if gamepadInput:
        sendGamepadCommand(gamepadInput)

    telemetry = reciveTelemetry()
    if telemetry is None:
        pass
    else:
        pass
