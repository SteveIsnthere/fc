from cmath import pi
import krpc
conn = krpc.connect(name='sim')
vessel = conn.space_center.active_vessel

def ksp_roll():
    return -vessel.flight().roll

def ksp_pitch():
    return vessel.flight().pitch

def ksp_heading():
    return vessel.flight().heading

def ksp_roll_speed():
    return vessel.angular_velocity(vessel.orbit.body.non_rotating_reference_frame)[0]/pi*180

def ksp_pitch_speed():
    return vessel.angular_velocity(vessel.orbit.body.non_rotating_reference_frame)[1]/pi*180

def ksp_heading_speed():
    return vessel.angular_velocity(vessel.orbit.body.non_rotating_reference_frame)[2]/pi*180


def ksp_altitude():
    return vessel.flight().mean_altitude

def ksp_temperature():
    return 15
    
def ksp_hspeed():
    return vessel.flight().speed

def ksp_vspeed():
    return vessel.flight().vertical_speed


def ksp_latitude():
    return vessel.flight().latitude

def ksp_longitude():
    return vessel.flight().longitude

def ksp_g_force():
    return vessel.flight().g_force


def ksp_set_pitch(input):
    vessel.control.pitch = input

def ksp_set_roll(input):
    vessel.control.roll = input

def ksp_set_throttle(input):
    vessel.control.throttle = input

class KSP_baro:
    @property
    def altitude(self):
        return ksp_altitude()
    @property
    def temperature(self):
        return ksp_temperature()

class KSP_gps:
    @property
    def latitude(self):
        return ksp_latitude()
    @property
    def longitude(self):
        return ksp_longitude()
    @property
    def has_fix(self):
        return True
    @property
    def satellites(self):
        return 15
    @property
    def altitude_m(self):
        return ksp_altitude()
    @property
    def speed_knots(self):
        return ksp_hspeed()/0.51444
    @property
    def track_angle_deg(self):
        #need further implemetation
        return ksp_heading()

    def update(self):
        return

class KSP_imu:
    @property
    def euler(self):
        return [ksp_heading(),ksp_pitch(),ksp_roll()]
    @property
    def gyro(self):
        return [ksp_roll_speed(),ksp_pitch_speed(),ksp_heading_speed()]
    @property
    def linear_acceleration(self):
        return [0,0,0]

class KSP_Pitot:
    @property
    def temperature(self):
        return 1
    @property
    def pressure(self):
        return 13

class KSP_lora:
    @property
    def pressure(self):
        return 1
    def receive(self,timeout):
        return
    def send(self,data):
        return


