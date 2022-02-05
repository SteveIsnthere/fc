import hid
import time
from multiprocessing import Value
from multiprocessing import Process
import serial
#radio = serial.Serial('/dev/cu.usbmodem101', baudrate=115200)
gamepad = hid.device()
gamepad.open(0x18d1,0x9400)
gamepad.set_nonblocking(True)

aileron_gain = 3 # can only be odd number
elevator_gain = 3 

control_mode = 1
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

def sendGamepadCommand(gamepadInput):
    global control_mode
    content = None
    left_arrow_pad = gamepadInput[1]
    multi_purpose1 = gamepadInput[2]
    multi_purpose2 = gamepadInput[3]
    stick1x = gamepadInput[4]
    stick1y = gamepadInput[5]
    stick2x = gamepadInput[6]
    stick2y = gamepadInput[7]
    leftupperpressure = gamepadInput[8]
    rightupperpressure = gamepadInput[9]

    if multi_purpose1 == 0:
        pass
    else:
        if multi_purpose1 == 4:#leftupperpressure pressed
            print('leftupperpressure pressed')
            return
        elif multi_purpose1 == 8:#rightupperpressure pressed
            print('rightupperpressure pressed')
            return
        elif multi_purpose1 == 12:# both upperpressure pressed 
            print('both upperpressure pressed')
            return
        elif multi_purpose1 == 64:# middle left 1
            print('middle left 1')
            return
        elif multi_purpose1 == 2:# middle left 2
            print('middle left 2')
            return
        elif multi_purpose1 == 32:# middle right 1
            print('middle right 1')
            return
        elif multi_purpose1 == 1:# middle right 2
            print('middle right 2')
            return
        elif multi_purpose1 == 16:# middle stadia
            # init the flight
            print('middle stadia')
            sendData("90")
            return
        elif multi_purpose1 == 128:# right stick pressed
            print('right stick pressed')
            return

    if multi_purpose2 == 0:
        pass
    else:
        if multi_purpose2 == 4:#leftupperbutton pressed
            # full manual mode
            print('leftupperbutton pressed')
            control_mode = 0
            return
        elif multi_purpose2 == 2:#rightupperbutton pressed
            # fly by wire (partial manual) mode
            print('rightupperbutton pressed')
            control_mode = 1
            return
        elif multi_purpose2 == 6:#both upperbutton pressed 
            print('both upperbutton pressed ')
            return
        elif multi_purpose2 == 8:#up (right)
            print('Y')
            return
        elif multi_purpose2 == 64:#down
            # TOGA MODE
            print('A')
            control_mode = 21
            sendData("21")
            return
        elif multi_purpose2 == 16:#left
            print('X')
            return
        elif multi_purpose2 == 32:#right
            print('B')
            return
        elif multi_purpose2 == 1:#left stick pressed
            print('left stick pressed')
            return

    if left_arrow_pad == 8:
        pass
    else:
        if left_arrow_pad == 0:#up
            print('arrow_pad up')
            return
        elif left_arrow_pad == 4:#down
            print('arrow_pad down')
            return
        elif left_arrow_pad == 6:#left
            print('arrow_pad left')
            return
        elif left_arrow_pad == 2:#right
            print('arrow_pad right')
            return
    
    # raw values out of 1
    throttle_raw = stick1y/255
    aileron_raw = stick2x/255
    elevator_raw = stick2y/255
    # out of 99
    throttle_cooked = int(throttle_raw*99)
    if throttle_cooked<10:
        throttle_cooked = "0"+str(throttle_cooked)
    elevator_cooked = int(elevator_raw*99)
    aileron_cooked = int(aileron_raw*99)
    if aileron_cooked<10:
        aileron_cooked = "0"+str(aileron_cooked)
    elevator_cooked = int(elevator_raw*99)
    if elevator_cooked<10:
        elevator_cooked = "0"+str(elevator_cooked)

    if control_mode == 0:
        command = "0"
        payload = str(aileron_cooked)+str(elevator_cooked)+str(throttle_cooked)
        content = command+payload
        sendData(content)

    

def reciveTelemetry():
    telemetry = None
    try:
        #telemetry = radio.readline().decode("ascii").split(",")
        print(telemetry)
    except:
        print("reciveTelemetry() Error")

while True:
    gamepadInput = gamepad.read(64)
    if gamepadInput:
        sendGamepadCommand(gamepadInput)
    #reciveTelemetry()


