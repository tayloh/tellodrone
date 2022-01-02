

from listener import MultikeyListener
from djitellopy import tello

import threading
import time
import cv2 as cv
import vision
import numpy as np

class DroneController:

    MOVE_FORW = "forward"
    MOVE_BACK = "backward"
    MOVE_LEFT = "left"
    MOVE_RIGHT = "right"
    MOVE_ROTLEFT = "rotateleft"
    MOVE_ROTRIGHT = "rotateright"
    MOVE_UP = "up"
    MOVE_DOWN = "down"
    MOVE_LAND = "land"
    MOVE_TAKEOFF = "takeoff"
    MOVE_BACKFLIP = "backflip"
    CONTROL_SPEEDUP = "speedup"
    CONTROL_SPEEDDOWN = "speeddown"
    CONTROL_TURNRATEDOWN = "turndown"
    CONTROL_TURNRATEUP = "turnup"

    MAX_SPEED = 100
    MIN_SPEED = 0

    KEY_MAPPINGS = {      
        "w" : MOVE_FORW,
        "s" : MOVE_BACK,
        "a" : MOVE_LEFT,
        "d" : MOVE_RIGHT,
        "q" : MOVE_ROTLEFT,
        "e" : MOVE_ROTRIGHT,
        "o" : MOVE_UP,
        "p" : MOVE_DOWN,
        "l" : MOVE_LAND,
        "t" : MOVE_TAKEOFF,
        "f" : MOVE_BACKFLIP,
        "2" : CONTROL_SPEEDUP,
        "1" : CONTROL_SPEEDDOWN,
        "3" : CONTROL_TURNRATEDOWN,
        "4" : CONTROL_TURNRATEUP
    }

    def __init__(self):
        self.input_handler = MultikeyListener()
        # self.drone = tello.Tello()
        self.control_thread = None
        self.telemetry_data = DroneTelemetry()
        self.is_on = False
        self.speed = 80
        self.turn_rate = 100
    
    def start(self):
        """Connects to drone and starts listening for input.
        """
        if self.is_on:
            print("[DroneController] Drone is already on")
        else:
            self.drone = tello.Tello()
            self.input_handler.start_listener() # daemon = True
            self.drone.connect()
            self.is_on = True
            print("[DroneController] Drone is connected")
            self.control_thread = threading.Thread(target=self._control_loop) 
            self.control_thread.start()
            print("[DroneController] Control thread started")      

    def start_video_stream(self):
        """Starts the drones video stream.
        """
        self.drone.streamon()

    def stop_video_stream(self):
        """Stops the drones video stream.
        """
        self.drone.streamoff()

    def get_stream_status(self):
        """Returns status of video stream (on/off).
        """
        return self.drone.stream_on
    
    def stop(self):
        """Lands the drone, turns off the stream.
        """
        if not self.is_on:
            print("[DroneController] Drone is already off")
        else:
            self.is_on = False
            self.control_thread.join()
            if self.drone.is_flying:
                self._land_nonblocking()
                self.drone.send_rc_control(0, 0, 0, 0)

            self.drone.streamoff()
            
            #self.drone.end() #this fucking fucks with everything?
            print("[DroneController] Control thread stopped")
    
    def get_video_frame(self):
        """Gets a frame from the drones video capture.
        """
        if self.drone.stream_on:
            return self.drone.get_frame_read().frame
        else:
            return None

    def get_drone_telemetry(self):
        """Gets the telemetry data.
        """
        return self.telemetry_data
    
    def _control_loop(self):
        """Main control loop.
        """
        while True:
            if not self.is_on:
                break

            actions = self._get_actions_from_keys()
            lr, fb, ud, rot = self._get_rc_vector_from_actions(actions)

            if DroneController.MOVE_TAKEOFF in actions:
                self._takeoff_nonblocking()
            elif DroneController.MOVE_LAND in actions:
                self._land_nonblocking()
            
            if DroneController.CONTROL_SPEEDUP in actions:
                if self.speed < DroneController.MAX_SPEED:
                    self.speed += 1
            elif DroneController.CONTROL_SPEEDDOWN in actions:
                if self.speed > DroneController.MIN_SPEED:
                    self.speed -= 1
            
            if DroneController.CONTROL_TURNRATEUP in actions:
                if self.turn_rate < DroneController.MAX_SPEED:
                    self.turn_rate += 1
            elif DroneController.CONTROL_TURNRATEDOWN in actions:
                if self.turn_rate > DroneController.MIN_SPEED:
                    self.turn_rate -= 1

            self.drone.send_rc_control(lr, fb, ud, rot)

            self._update_telemetry_from_drone()
            time.sleep(0.05)

    def _land_nonblocking(self):
        """Lands the drone while still being able to take rc input.
        """
        landing_thread = threading.Thread(target=self.drone.land)
        landing_thread.start()
    
    def _takeoff_nonblocking(self):
        """Takes off the drone while still being able to take rc input.
        """
        takeoff_thread = threading.Thread(target=self.drone.takeoff)
        takeoff_thread.start()
    
    def _get_rc_vector_from_actions(self, actions):
        """Gets the rc control vector from a list of actions.
        """
        vector = [0, 0, 0, 0]
        if DroneController.MOVE_FORW in actions:
            vector[1] = self.speed
        elif DroneController.MOVE_BACK in actions:
            vector[1] = -self.speed
        
        if DroneController.MOVE_LEFT in actions:
            vector[0] = -self.speed
        elif DroneController.MOVE_RIGHT in actions:
            vector[0] = self.speed
        
        if DroneController.MOVE_UP in actions:
            vector[2] = self.speed
        elif DroneController.MOVE_DOWN in actions:
            vector[2] = -self.speed
        
        if DroneController.MOVE_ROTLEFT in actions:
            vector[3] = -self.turn_rate
        elif DroneController.MOVE_ROTRIGHT in actions:
            vector[3] = self.turn_rate
        
        return vector[0], vector[1], vector[2], vector[3]


    def _get_actions_from_keys(self):
        """Gets the actions associated with each currently pressed key.
        """
        actions = []
        for key_input in self.input_handler.get_pressed():
            if key_input in DroneController.KEY_MAPPINGS.keys():
                actions.append(DroneController.KEY_MAPPINGS[key_input])
        return actions
    
    
    def _update_telemetry_from_drone(self):
        """Grabs telemetry data from the drone.
        """
        self.telemetry_data.pitch = self.drone.get_pitch()
        self.telemetry_data.roll = self.drone.get_roll()
        self.telemetry_data.yaw = self.drone.get_yaw()
        self.telemetry_data.speed_z = self.drone.get_speed_z()
        self.telemetry_data.acc_x = self.drone.get_acceleration_x()
        self.telemetry_data.acc_y = self.drone.get_acceleration_y()
        self.telemetry_data.acc_z = self.drone.get_acceleration_z()
        self.telemetry_data.temp = self.drone.get_temperature()
        self.telemetry_data.height = self.drone.get_height()
        self.telemetry_data.tof_dist = self.drone.get_distance_tof()
        self.telemetry_data.abs_height = self.drone.get_barometer()
        self.telemetry_data.battery = self.drone.get_battery()
        self.telemetry_data.flight_time = self.drone.get_flight_time()
        self.telemetry_data.speedp = self.speed
        self.telemetry_data.turnp = self.turn_rate



class DroneView:
    """
    View the video stream of the drone along with a HUD containing
    telemetry.
    """
    # TODO Move droneview to own file with all gui related stuff.
    # TODO Use Tkinter for the gui.
    GREEN = (0, 255, 0)
    BLANK = np.zeros(shape=(720, 960, 3), dtype=np.uint8)
    FACEDETECTION_WAITTIME = 0.05

    def __init__(self, drone):
        self.drone = drone

        self.has_facerects = False
        self.facerects_last = ()
        self.facerects = ()
        self.facedetection_thread = None
        self.detect_faces = False
    
    def detect_faces_on(self):
        """Turns on face detection.
        """
        if self.drone.get_stream_status():
            self.detect_faces = True
            self.facedetection_thread = threading.Thread(target=self._face_detection)
            self.facedetection_thread.start()
            print("[DroneView] Face detect thread started")
        else:
            print("[DroneView] Video stream is off")

    def detect_faces_off(self):
        """Turns off face detection.
        """
        if self.detect_faces_on:
            self.detect_faces = False # -> stops facedetection thread
            self.facedetection_thread.join()

            self.has_facerects = False
            self.facerects_last = () # -> reset rectangles
            print("[DroneView] Face detect thread stopped")
        else:
            print("[DroneView] Face detection is already off")

    def show_drone_view(self):
        """Shows the drones view along with HUD.
        """
        frame = DroneView.BLANK

        if not self.drone.is_on:
            return frame

        if self.drone.get_stream_status():
            try:
                frame = self.drone.get_video_frame()
            except:
                print("[DroneView] Tello failed to grab first frame")

        data = self.drone.get_drone_telemetry()

        if self.detect_faces and self.has_facerects:
            self.facerects_last = self.facerects
            # self.facerects = () not needed
            self.has_facerects = False
        
        frame = self._draw_face_rects(frame, self.facerects_last)
        frame = self._draw_battery(frame, data.battery)
        frame = self._draw_flight_telemetry(frame, data)
        frame = self._draw_crosshair(frame)

        #cv.imshow("drone view", frame)
        #cv.waitKey(1)
        frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
        return frame

    def exit_view(self):
        self.detect_faces_off()
        cv.waitKey(1000)
        cv.destroyAllWindows()

    def _draw_battery(self, frame, battery):
        """Draws graphical view of battery percentage.
        """
        frame_width = frame.shape[1]
        frame_height = frame.shape[0]

        b_maxlength = frame_width // 5
        b_height = 15
        b_length = int((battery / 100) * b_maxlength)
        x_pos = frame_width // 100
        y_pos = frame_height // 20

        cv.putText(frame, str(battery), (x_pos + b_maxlength + 10, y_pos + 14), cv.FONT_HERSHEY_PLAIN,
        1, DroneView.GREEN, 1, cv.LINE_AA)

        cv.rectangle(frame, (x_pos, y_pos), (x_pos + b_length, y_pos + b_height), DroneView.GREEN, -1)
        cv.rectangle(frame, (x_pos, y_pos), (x_pos + b_maxlength, y_pos + b_height), DroneView.GREEN, 2)

        return frame

    def _draw_flight_telemetry(self, frame, tel):
        """Draws flight telemetry text on frame.
        """
        frame_width = frame.shape[1]
        frame_height = frame.shape[0]

        x_pos = frame_width // 100
        y_pos_start = (frame_height // 20) + 40
        y_delta = 20

        telemetry_dict = tel.get_telemetry_as_dict()
        for i, key in enumerate(telemetry_dict.keys()):
            if key != "battery":
                text = key + " : " + telemetry_dict[key]
                cv.putText(frame, text, (x_pos, y_pos_start + y_delta*i),
                cv.FONT_HERSHEY_PLAIN, 1, DroneView.GREEN, 1, cv.LINE_AA)

        return frame
    
    def _draw_crosshair(self, frame):
        """Draws a crosshair in the middle of the frame.
        """
        size = 15
        horiz_p1 = (frame.shape[1]//2 - size, frame.shape[0]//2) 
        horiz_p2 = (frame.shape[1]//2 + size, frame.shape[0]//2) 
        vert_p1 = (frame.shape[1]//2, frame.shape[0]//2 - size)
        vert_p2 = (frame.shape[1]//2, frame.shape[0]//2 + size)
        cv.line(frame, horiz_p1, horiz_p2, DroneView.GREEN, 2)
        cv.line(frame, vert_p1, vert_p2, DroneView.GREEN, 2)

        return frame
    
    def _draw_face_rects(self, frame, rects):
        """Draws rectangles on frame.
        """
        for x, y, w, h in rects:
            cv.rectangle(frame, (x, y), (x + w, y + h), DroneView.GREEN, 2)
        
        return frame

    def _face_detection(self):
        """Runs face detection.
        """
        while self.detect_faces:
            try:
                img = self.drone.get_video_frame()
                self.facerects = vision.haar_detect_faces_frontal(img)
                self.has_facerects = True
            except:
                print("[DroneView] Tello failed to grab first frame")
            time.sleep(DroneView.FACEDETECTION_WAITTIME)


class DroneTelemetry:
    """Collection of flight telemetry data.
    """
    
    def __init__(self):
        self.pitch = 0
        self.roll = 0
        self.yaw = 0
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
        """Gets telemetry data as dictionary.
        """
        dct = {
            "pitch" : str(self.pitch),
            "roll" : str(self.roll),
            "yaw" : str(self.yaw),
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