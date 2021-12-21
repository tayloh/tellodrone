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
    # TODO: graceful exit, maybe
    isStarted = False

    if not testing:
        drone = tello.Tello()

        print("Attempting to connect to drone...")
        drone.connect()
        print("Connected.")
        drone.streamon()

    while True:

        # VIEW/CAMERA
        frame = drone.get_frame_read().frame

        view.set_info_text("Battery: " + str(drone.get_battery()))
        view.set_info_text("Speed X: " + str(drone.get_speed_x()))
        view.set_info_text("Speed Y: " + str(drone.get_speed_y()))
        view.set_info_text("Speed Z: " + str(drone.get_speed_z()))
        view.set_info_text("Height: " + str(drone.get_height()))
        view.set_info_text("Flight time: " + str(drone.get_flight_time()))
        view.get_view(frame)

        # MOVEMENT
        actions = mm.get_movement_actions()
        lr, fb, ud, yaw, tl, bf  = mm.get_rc_output_vector(actions)
        
        if not testing:
            
            # takeoff and landing
            if tl == 1 and not isStarted:
                # blocking action, needs own thread
                takeoff_thread = threading.Thread(target=drone.takeoff)
                takeoff_thread.start()
                isStarted = True
                #drone.takeoff()

            elif tl == 2 and isStarted:
                landing_thread = threading.Thread(target=drone.land)
                landing_thread.start()
                isStarted = False
                #drone.land()
            
            if bf == 1:
                # TODO: gracefully tell the user it couldnt do bf
                backflip_thread = threading.Thread(target=drone.flip_back)
                backflip_thread.start()
                #drone.flip_back()

            drone.send_rc_control(lr, fb, ud, yaw)
        
        if testing:
            #pass
            print(lr, fb, ud, yaw, tl)

        time.sleep(0.05)




if __name__ == "__main__":
    main()