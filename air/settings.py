control_loop_freq = 50
secondary_loop_freq = 10
gps_loop_freq = 5
manual_control_update_freq = 15

# autoland&rth
rth_altitude = 100  # meters
touch_down_from_launch_distance = 20  # meters
glide_slope = 20  # degrees

# hand launch
toga_thrust = 0.75
toga_pitch = 15

# performance
roll_authority = 30  # degrees per second
pitch_authority = 20
yaw_authority = 5

aileronTrim = 0  # 0-1
elevatorTrim = 0

control_softness = 1  # time to align in seconds

min_airspeed = 15/3.6  # meters per second
normal_BankAngle = 30
max_BankAngle = 45
normal_pitch = 20
max_pitch = 25
max_aoa = 13

# sensor
# imu
angular_velocity_data_smooth_out = 0.9  # 0.99-0.01
IMU_acc_data_smooth_out = 0.9
attitude_data_smooth_out = 0.8

# Baro
Baro_altitude_data_smooth_out = 0.9
Baro_vertical_speed_data_smooth_out = 0.9
Baro_temperature_data_smooth_out = 0.9

# Control Surfaces
ailerons_mid_point = 90
ailerons_actuation_range = 30
ailerons_actuation_limit = 50

elevators_mid_point = 90
elevators_actuation_range = 40
elevators_actuation_limit = 60
