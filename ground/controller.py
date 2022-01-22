import hid

# uncomment below to check for usb devices ids
# for device in hid.enumerate():
#     print(f"0x{device['vendor_id']:04x}:0x{device['product_id']:04x} {device['product_string']}")

gamepad = hid.device()
gamepad.open(0x18d1, 0x9400)
gamepad.set_nonblocking(True)

gamePadCommand = None

while True:
    gamepadInput = gamepad.read(64)
    if gamepadInput:
        gamePadCommand = gamepadInput


"""
[#,left_arrow_pad,multi_purpose1,multi_purpose2,stick1x,stick1y,stick2x,stick2y,leftupperpressure(0-255),rightupperpressure(0-255),#]

left_arrow_pad:
8:nothing
0:up
4:down
6:left
2:right

multi_purpose1:
0:nothing
4:leftupperpressure pressed
8:rightupperpressure pressed
12: both upperpressure pressed 
64: middle left 1
2: middle left 2
32: middle right 1
1: middle right 2
16: middle stadia
128: right stick pressed

multi_purpose2:
0:nothing
4:leftupperbutton pressed
2:rightupperbutton pressed
6:both upperbutton pressed 
8:up (right)
64:down 
16:left
32:right
1:left stick pressed
"""