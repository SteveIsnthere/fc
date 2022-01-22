from init import *

import csv
from multiprocessing import Process


def level0ControlLoop():
    # shared
    # telemetry
    global shared_pitch
    global shared_roll
    global shared_imu_heading
    # commands
    global flight_mode
    global desired_pitch
    global desired_roll

    # internal
    in_manual_control_mode = False
    # special cases
    exceed_Max_BankAngle = False
    stall = False
    # attitude
    pitch = 0
    roll = 0
    heading = 0
    last_pitch = 0
    last_roll = 0
    last_heading = 0
    attitude_new_data_weight = 1 - attitude_data_smooth_out
    # angular velocity
    pitch_speed = None
    roll_speed = None
    yaw_speed = None
    last_pitch_speed = 0
    last_roll_speed = 0
    last_yaw_speed = 0
    angular_velocity_new_data_weight = 1 - angular_velocity_data_smooth_out
    # linear acceleration
    IMU_acc_x = None
    IMU_acc_y = None
    IMU_acc_z = None
    last_IMU_acc_x = 0
    last_IMU_acc_y = 0
    last_IMU_acc_z = 0
    IMU_acc_new_data_weight = 1 - IMU_acc_data_smooth_out
    # relative linear acceleration
    acc_x = None
    acc_y = None
    acc_z = None
    # controls
    desired_pitch_internal = 0
    desired_roll_internal = 0
    aileron_trim = aileronTrim.value
    elevator_trim = elevatorTrim.value
    aileron_input = None
    elevator_input = None
    manual_aileron_input_internal = 0
    manual_elevator_input_internal = 0
    raw_aileron_input = None
    raw_elevator_input = None

    last_control_loop_update_time = time.monotonic()
    last_secondary_loop_update_time = time.monotonic()

    while True:
        current_time = time.monotonic()
        control_loop_elapsed = current_time - last_control_loop_update_time
        secondary_loop_elapsed = current_time - last_secondary_loop_update_time

        # control_loop
        if control_loop_elapsed > control_loop_interval:
            last_control_loop_update_time = current_time
            # print(control_loop_elapsed)
            
            # IMU
            # attitude
            imu_attitute = imu.euler

            pitch_ = imu_attitute[1]
            if pitch_ is not None and pitch_ <= 90 and pitch_ >= -90:
                pitch = (
                    pitch_ * attitude_new_data_weight
                    + last_pitch * attitude_data_smooth_out
                )
                last_pitch = pitch

            roll_ = imu_attitute[2]
            if roll_ is not None and roll_ <= 180 and roll_ >= -180:
                roll_ = -roll_
                if roll_ * last_roll > 0:
                    roll = (
                        roll_ * attitude_new_data_weight
                        + last_roll * attitude_data_smooth_out
                    )
                else:  # 180 -> -180
                    roll = roll_
                last_roll = roll

            heading_ = imu_attitute[0]
            if heading_ is not None and heading_ <= 360 and heading_ >= 0:
                heading = (
                    heading_ * attitude_new_data_weight
                    + last_heading * attitude_data_smooth_out
                )
                last_heading = heading

            # angular velocity
            imu_angular_velocity = imu.gyro  # [roll,pitch,yaw]

            roll_speed_ = imu_angular_velocity[0]
            if roll_speed_ is not None:
                roll_speed = (
                    roll_speed_ * angular_velocity_new_data_weight
                    + last_roll_speed * angular_velocity_data_smooth_out
                )
                last_roll_speed = roll_speed

            pitch_speed_ = imu_angular_velocity[1]
            if pitch_speed_ is not None:
                pitch_speed = (
                    pitch_speed_ * angular_velocity_new_data_weight
                    + last_pitch_speed * angular_velocity_data_smooth_out
                )
                last_pitch_speed = pitch_speed

            yaw_speed_ = imu_angular_velocity[2]
            if yaw_speed_ is not None:
                yaw_speed = (
                    yaw_speed_ * angular_velocity_new_data_weight
                    + last_yaw_speed * angular_velocity_data_smooth_out
                )
                last_yaw_speed = yaw_speed

            # linear_acceleration
            imu_acc = imu.linear_acceleration

            IMU_acc_x_ = imu_acc[0]
            if IMU_acc_x_ is not None:
                IMU_acc_x = (
                    IMU_acc_x_ * IMU_acc_new_data_weight
                    + last_IMU_acc_x * IMU_acc_data_smooth_out
                )
                last_IMU_acc_x = IMU_acc_x

            IMU_acc_y_ = imu_acc[1]
            if IMU_acc_y_ is not None:
                IMU_acc_y = (
                    IMU_acc_y_ * IMU_acc_new_data_weight
                    + last_IMU_acc_y * IMU_acc_data_smooth_out
                )
                last_IMU_acc_y = IMU_acc_y

            IMU_acc_z_ = imu_acc[2]
            if IMU_acc_z_ is not None:
                IMU_acc_z = (
                    IMU_acc_z_ * IMU_acc_new_data_weight
                    + last_IMU_acc_z * IMU_acc_data_smooth_out
                )
                last_IMU_acc_z = IMU_acc_z

            # relative linear acceleration
            acc_x = None
            acc_y = None
            acc_z = None
            # controls
            if not in_manual_control_mode:
                # check for special cases
                if roll < max_BankAngle / 2 and roll > -max_BankAngle / 2:
                    exceed_Max_BankAngle = False
                elif roll > max_BankAngle or roll < -max_BankAngle:
                    exceed_Max_BankAngle = True

                    # translate to rawinputs
                if not exceed_Max_BankAngle:  # normal flight
                    aileron_input = controlInputRequired(
                        roll,
                        roll_speed,
                        desired_roll_internal,
                        control_softness,
                        roll_authority,
                    )
                    elevator_input = controlInputRequired(
                        pitch,
                        pitch_speed,
                        desired_pitch_internal,
                        control_softness,
                        pitch_authority,
                    )
                else:  # exceed_Max_BankAngle
                    # ease load, level the wing
                    aileron_input = controlInputRequired(
                        roll,
                        roll_speed,
                        0,
                        control_softness / 2,
                        roll_authority * 0.75,
                    )
                    elevator_input = 0

                raw_aileron_input = aileron_input
                raw_elevator_input = elevator_input

                if raw_aileron_input > 1:  # raw control capped out at 100%
                    raw_aileron_input = 1
                elif raw_aileron_input < -1:
                    raw_aileron_input = -1

                if raw_elevator_input > 1:
                    raw_elevator_input = 1
                elif raw_elevator_input < -1:
                    raw_elevator_input = -1

                    # execute the controls
                aileron_actuation(raw_aileron_input, aileron_trim)
                elevator_actuation(raw_elevator_input, elevator_trim)

        # secondary loop
        if secondary_loop_elapsed > secondary_loop_interval:
            last_secondary_loop_update_time = current_time
            # print(secondary_loop_elapsed)
            if flight_mode.value == 0:
                in_manual_control_mode = True
            else:
                in_manual_control_mode = False

            # share the telemetry
            shared_pitch.value = pitch
            shared_roll.value = roll
            shared_imu_heading.value = heading
            shared_raw_aileron_input.value = raw_aileron_input
            shared_raw_elevator_input.value = raw_elevator_input
            # fetch the commands
            desired_pitch_internal = desired_pitch.value
            desired_roll_internal = desired_roll.value
            aileron_trim = aileronTrim.value
            elevator_trim = elevatorTrim.value
            # print(raw_elevator_input)


def higherlevelControlLoop():
    # sensors
    global Baro_altitude
    global last_Baro_altitude
    Baro_altitude_new_data_weight = 1 - Baro_altitude_data_smooth_out
    global Baro_vertical_speed
    global last_Baro_vertical_speed
    Baro_vertical_speed_new_data_weight = 1 - Baro_vertical_speed_data_smooth_out
    global Baro_temperature
    global last_Baro_temperature
    Baro_temperature_new_data_weight = 1 - Baro_temperature_data_smooth_out
    global Pitot_pressure
    global Pitot_temperature
    global GPS_locked
    global GPS_latitude
    global GPS_longitude
    global GPS_satellites
    global GPS_altitude
    global GPS_speed
    global GPS_heading
    global GPS_coord_x
    global GPS_coord_y
    # Flight control
    global readyToArm
    global readyToFly
    global desired_roll
    global desired_pitch
    global desired_heading
    global desired_vs

    higherlevelControl_loop_interval = 1 / secondary_loop_freq
    gps_loop_interval = 1 / gps_loop_freq
    last_higherlevelControl_loop_update_time = time.monotonic()
    last_gps_loop_update_time = time.monotonic()
    blackBox_startingTimeStamp = time.monotonic()

    with open("fc/air/blackBox.csv", "w") as blackBox:
        blackBoxWriter = csv.writer(blackBox, delimiter=",")
        blackBoxWriter.writerow(
            [
                "time",
                "pitch",
                "roll",
                "heading",
                "aileronInput",
                "elevatorInput",
                "Baro_altitude",
                "Baro_vertical_speed",
                "Baro_temperature",
                "GPS_locked",
                "GPS_coord_x",
                "GPS_coord_y",
                "GPS_altitude",
                "GPS_heading",
                "GPS_speed",
                "GPS_satellites",
                "aileronTrim",
                "elevatorTrim"
            ]
        )  # header
        while True:
            current_time = time.monotonic()
            higherlevelControl_loop_elapsed = current_time - \
                last_higherlevelControl_loop_update_time
            gps_loop_elapsed = current_time - last_gps_loop_update_time
            # sensor update & #Flight control
            if higherlevelControl_loop_elapsed > higherlevelControl_loop_interval:
                last_higherlevelControl_loop_update_time = current_time
                # print(higherlevelControl_loop_elapsed)
                # Baro
                Baro_altitude_ = barometer.altitude
                if Baro_altitude_ is not None:
                    Baro_altitude.value = (
                        last_Baro_altitude * Baro_altitude_data_smooth_out
                        + Baro_altitude_ * Baro_altitude_new_data_weight
                    )
                    Baro_vertical_speed.value = (
                        (Baro_altitude.value - last_Baro_altitude)
                        * Baro_vertical_speed_new_data_weight
                        + last_Baro_vertical_speed
                        * higherlevelControl_loop_elapsed
                        * Baro_vertical_speed_data_smooth_out
                    ) / higherlevelControl_loop_elapsed
                    last_Baro_vertical_speed = Baro_vertical_speed.value
                    last_Baro_altitude = Baro_altitude.value
                Baro_temperature_ = barometer.temperature
                if Baro_temperature_ is not None:
                    Baro_temperature.value = (
                        last_Baro_temperature * Baro_altitude_data_smooth_out
                        + Baro_temperature_ * Baro_temperature_new_data_weight
                    )
                    last_Baro_temperature = Baro_temperature.value
                # Pitot
                Pitot_pressure_ = pitot.pressure
                if Pitot_pressure_ is not None:
                    Pitot_pressure.value = Pitot_pressure_
                Pitot_temperature_ = pitot.temperature
                if Pitot_temperature_ is not None:
                    Pitot_temperature.value = Pitot_temperature_

                # Flight control
                # readyToArm
                if not bool(readyToArm.value):
                    time_since_start_up = time.time()-start_up_time
                    if time_since_start_up > 10 and GPS_locked.value == 1:
                        readyToArm.value = 1

                if bool(readyToFly.value):
                    # throttle
                    if bool(manual_throttle_unlocked.value):
                        throttle_control(manual_throttle_input.value)
                    else:
                        throttle_control(desired_throttle.value)
                    # level2ControlLoop
                    if flight_mode.value == 1:
                        desired_pitch.value += manual_pitch_change_per_sec.value * \
                            higherlevelControl_loop_interval
                        desired_roll.value += manual_roll_change_per_sec.value * \
                            higherlevelControl_loop_interval
                    else:
                        heading_diff = desired_heading.value - GPS_heading.value
                        vs_diff = desired_vs.value - Baro_vertical_speed.value

                    if desired_roll.value > normal_BankAngle:
                        desired_roll.value = normal_BankAngle
                    elif desired_roll.value < -normal_BankAngle:
                        desired_roll.value = -normal_BankAngle

                    if desired_pitch.value > normal_pitch:
                        desired_pitch.value = normal_pitch
                    elif desired_pitch.value < -normal_pitch:
                        desired_pitch.value = -normal_pitch
                    # level3ControlLoop

            if gps_loop_elapsed > gps_loop_interval:
                last_gps_loop_update_time = current_time
                # print(gps_loop_elapsed)
                gps.update()
                # Every second print out current location details if there's a fix.
                if not gps.has_fix:
                    GPS_locked.value = 0
                else:
                    GPS_locked.value = 1
                    GPS_latitude.value = gps.latitude
                    GPS_longitude.value = gps.longitude
                    GPS_coord_x.value, GPS_coord_y.value, _, _ = utm.from_latlon(
                        GPS_latitude.value, GPS_longitude.value
                    )
                    # print("Fix quality: {}".format(gps.fix_quality))
                    # Some attributes beyond latitude, longitude and timestamp are optional
                    # and might not be present.  Check if they're None before trying to use!
                    if gps.satellites is not None:
                        GPS_satellites.value = gps.satellites
                    if gps.altitude_m is not None:
                        GPS_altitude.value = gps.altitude_m
                    if gps.speed_knots is not None:
                        GPS_speed.value = gps.speed_knots * 0.51444
                    if gps.track_angle_deg is not None:
                        GPS_heading.value = gps.track_angle_deg

                # data recorder (blackBox)
                if True:  # readyToFly
                    timeStamp = round(
                        current_time - blackBox_startingTimeStamp, 3)
                    record = [
                        timeStamp,
                        round(shared_pitch.value, 2),
                        round(shared_roll.value, 2),
                        round(shared_imu_heading.value, 2),
                        round(shared_raw_aileron_input.value, 2),
                        round(shared_raw_elevator_input.value, 2),
                        round(Baro_altitude.value, 2),
                        round(Baro_vertical_speed.value, 2),
                        round(Baro_temperature.value, 2),
                        int(GPS_locked.value),
                        round(GPS_coord_x.value, 2),
                        round(GPS_coord_y.value, 2),
                        round(GPS_altitude.value, 2),
                        round(GPS_heading.value, 2),
                        round(GPS_speed.value, 2),
                        int(GPS_satellites.value),
                        round(aileronTrim.value, 2),
                        round(elevatorTrim.value, 2),
                    ]
                    blackBoxWriter.writerow(record)
                    # print("wrote at "+str(timeStamp))


def commLoop():
    global telemetry_mode
    global last_received_upLink
    global since_last_received_upLink

    global readyToFly
    global flight_mode
    global manual_throttle_unlocked

    global manual_throttle_input

    global manual_roll_change_per_sec
    global manual_pitch_change_per_sec

    global circle_altitude
    global desired_throttle

    global aileronTrim
    global elevatorTrim
    while True:
        receivedPacket = None
        receivedContent = None
        contentToSent = ""
        packetToSent = None

        try:
            receivedPacket = rfm9x.receive(timeout=5.0)  # default timeout=.5
            if receivedPacket is not None:
                receivedContent = receivedPacket.decode("ascii")
                tele_command = receivedContent[0]
                tele_payload = receivedContent[1:]
                # last update time
                received_time = time.time()
                since_last_received_upLink.value = received_time - last_received_upLink
                last_received_upLink = received_time

                if tele_command == '0':  # full manual
                    if flight_mode.value != 0:
                        manual_throttle_unlocked.value = 1
                        flight_mode.value = 0
                    manual_aileron_input = float(tele_payload[0:2])*0.01
                    manual_elevator_input = float(tele_payload[2:4])*0.01
                    manual_throttle_input.value = float(tele_payload[4:6])*0.01
                    aileron_actuation(manual_aileron_input, aileronTrim.value)
                    elevator_actuation(
                        manual_elevator_input, elevatorTrim.value)
                elif tele_command == '1':  # fly by wire (partial manual)
                    if flight_mode.value != 1:
                        manual_throttle_unlocked.value = 0
                        flight_mode.value = 1
                    manual_roll_change_per_sec.value = float(tele_payload[0:2])
                    manual_pitch_change_per_sec.value = float(
                        tele_payload[2:4])
                    manual_throttle_input.value = float(tele_payload[4:6])*0.01
                elif tele_command == '2':  # fully auto modes
                    fully_auto_mode = int(tele_payload[0])
                    mode_num = fully_auto_mode+2
                    if flight_mode.value != mode_num:
                        manual_throttle_unlocked.value = 0
                        flight_mode.value = mode_num
                        if mode_num == 3:
                            circle_altitude.value = GPS_altitude.value
                        elif mode_num == 4:
                            desired_throttle.value = toga_thrust
                elif tele_command == '9':  # Change Settings
                    param_index = int(tele_payload[0:2])
                    param_value = int(tele_payload[2:4])

                    # init the flight
                    if param_index == 0 and bool(readyToArm.value):
                        readyToFly.value = 1
                    elif param_index == 1:
                        aileronTrim.value += 0.01*param_value
                    elif param_index == 2:
                        elevatorTrim.value += 0.01*param_value

            else:
                continue
        except:
            continue

        if telemetry_mode != 0:
            try:
                packetToSent = contentToSent.encode("ascii")
                rfm9x.send(packetToSent)
            except:
                continue


thread1 = Process(target=level0ControlLoop)
thread2 = Process(target=higherlevelControlLoop)
thread3 = Process(target=commLoop)

thread1.start()
thread2.start()
thread3.start()
