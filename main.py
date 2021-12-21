"""
dont know exactly what I'll build yet, but it'll be something with
the tello drone and api.
"""

import logging # want to do flight logging
import threading
import time

from djitellopy import tello

import movement_model as mm
import view

testing = False

def main():
    if not testing:
        drone = tello.Tello()

        print("Attempting to connect to drone...")
        drone.connect()
        print("Connected.")
        drone.streamon()

    while True:

        # VIEW/CAMERA
        frame = drone.get_frame_read().frame

        view.set_info_text(str(drone.get_battery()))
        view.get_view(frame)

        # MOVEMENT
        actions = mm.get_movement_actions()
        lr, fb, ud, yaw, tl  = mm.get_rc_output_vector(actions)
        
        if not testing:
            
            # takeoff and landing
            if tl == 1:
                drone.takeoff()
            elif tl == 2:
                drone.land()
            
            drone.send_rc_control(lr, fb, ud, yaw)
        
        if testing:
            #pass
            print(lr, fb, ud, yaw, tl)

        time.sleep(0.05)




if __name__ == "__main__":
    main()