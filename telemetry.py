"""
created a class for this so that if other modules need all of the data I can just
pass an object with all of it basically
"""

class Telemetry:

    def __init__(self) -> None:
        self.pitch = 0
        self.roll = 0
        self.yaw = 0
        self.speed_x = 0
        self.speed_y = 0
        self.speed_z = 0
        self.acc_x = 0
        self.acc_y = 0
        self.acc_z = 0
        self.temp = 0
        self.height = 0
        self.tof_dist = 0
        self.abs_height = 0
        self.battery = 0
        self.flight_time = 0
        self.speedp = 0 #speed percentage of max
        self.turnp = 0 #turn percentage of max
    
    def get_telemetry_as_dict(self):
        dct = {
            "pitch" : str(self.pitch),
            "roll" : str(self.roll),
            "yaw" : str(self.yaw),
            "speed_x" : str(self.speed_x),
            "speed_y" : str(self.speed_y),
            "speed_z" : str(self.speed_z),
            "acc_x" : str(self.acc_x),
            "acc_y" : str(self.acc_y),
            "acc_z" : str(self.acc_z),
            "temp" : str(self.temp),
            "height" : str(self.height),
            "tof_dist" : str(self.tof_dist),
            "abs_height" : str(self.abs_height),
            "battery" : str(self.battery),
            "flight_time" : str(self.flight_time),
            "speedp" : str(self.speedp),
            "turnp" : str(self.turnp)
        }

        return dct
