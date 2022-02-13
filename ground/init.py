from radio_setup_ksp import *
import hid
import os
gamepad = hid.device()
gamepad.open(0x18d1,0x9400)
gamepad.set_nonblocking(True)

control_mode = 1

telemetryRecorder_path = os.path.join(os.path.expanduser('~'), "telemetryRecorder.csv")

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
            return
        elif multi_purpose1 == 8:#rightupperpressure pressed
            return
        elif multi_purpose1 == 12:# both upperpressure pressed 
            return
        elif multi_purpose1 == 64:# middle left 1
            return
        elif multi_purpose1 == 2:# middle left 2
            return
        elif multi_purpose1 == 32:# middle right 1
            return
        elif multi_purpose1 == 1:# middle right 2
            return
        elif multi_purpose1 == 16:# middle stadia
            # init the flight
            sendData("90")
            return
        elif multi_purpose1 == 128:# right stick pressed
            return

    if multi_purpose2 == 0:
        pass
    else:
        if multi_purpose2 == 4:#leftupperbutton pressed
            # full manual mode
            control_mode = 0
            return
        elif multi_purpose2 == 2:#rightupperbutton pressed
            # fly by wire (partial manual) mode
            control_mode = 1
            return
        elif multi_purpose2 == 6:#both upperbutton pressed 
            return
        elif multi_purpose2 == 8:#up (right)
            return
        elif multi_purpose2 == 64:#down
            # TOGA MODE
            control_mode = 21
            sendData("21")
            return
        elif multi_purpose2 == 16:#left
            return
        elif multi_purpose2 == 32:#right
            return
        elif multi_purpose2 == 1:#left stick pressed
            return

    if left_arrow_pad == 8:
        pass
    else:
        if left_arrow_pad == 0:#up
            sendData("920")
            return
        elif left_arrow_pad == 4:#down
            sendData("921")
            return
        elif left_arrow_pad == 6:#left
            sendData("910")
            return
        elif left_arrow_pad == 2:#right
            sendData("911")
            return
    
    # raw values out of 1
    throttle_raw = 1-stick1y/255
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