from msilib.schema import Control
import hid
from multiprocessing import Value
from multiprocessing import Process
import serial
radio = serial.Serial('/dev/cu.usbmodem101', baudrate=115200)
gamepad = hid.device()
gamepad.open(0x18d1, 0x9400)
gamepad.set_nonblocking(True)

aileron_gain = 3 # can only be odd number
elevator_gain = 3 


def controller_radioLoop():
    control_mode = 1
    def sendData(content):
        try:
            package = content.encode("ascii")
            radio.write(package)
        except:
            pass

    def sendGamepadCommand(gamepadInput):
        content = None
        left_arrow_pad = gamepadInput[1]
        multi_purpose1 = gamepadInput[2]
        multi_purpose2 = gamepadInput[3]
        multi_purpose2 = gamepadInput[4]
        stick1x = gamepadInput[5]
        stick1y = gamepadInput[6]
        stick2x = gamepadInput[7]
        stick2y = gamepadInput[8]
        leftupperpressure = gamepadInput[9]
        rightupperpressure = gamepadInput[10]
        if multi_purpose1 == 0:
            pass

        if multi_purpose2 == 0:
            pass

        if left_arrow_pad == 8:
            pass
        
        # raw values out of 1
        throttle_raw = stick1y/255
        aileron_raw = stick2x/255
        elevator_raw = stick2y/255
        # out of 99
        aileron_cooked = int(aileron_raw**aileron_gain*99)
        elevator_cooked = int(elevator_raw**elevator_gain*99)
        if control_mode == 0:
            command = "0"
            payload = str(aileron_cooked)+str(elevator_cooked)
            content = command+payload
            sendData(content)

        

    def reciveTelemetry():
        telemetry = None
        try:
            telemetry = radio.readline().decode("ascii").split(",")
            print(telemetry)
        except:
            pass

    while True:
        gamepadInput = gamepad.read(64)
        if gamepadInput:
            sendGamepadCommand(gamepadInput)
        reciveTelemetry()


thread1 = Process(target=controller_radioLoop)
thread1.start()
