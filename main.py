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
import telemetry

testing = False

def main():

    # TODO: graceful exit, maybe
    flying = False
    camera_dir = tello.Tello.CAMERA_FORWARD

    if not testing:
        drone = tello.Tello()

        print("Attempting to connect to drone...")
        drone.connect()
        print("Connected.")
        drone.streamon()
    

    while True:

        # MOVEMENT AND ACTIONS
        actions = mm.get_movement_actions()
        lr, fb, ud, rot = mm.get_rc_output_vector(actions)
        takeoff, land, bf, ex, swpcam = mm.get_aux_action_vector(actions)
        
        if not testing:
            
            tel = telemetry.Telemetry()

            # TELEMETRY
            tel.pitch = drone.get_pitch()
            tel.roll = drone.get_roll()
            tel.yaw = drone.get_yaw()
            tel.speed_x = drone.get_speed_x()
            tel.speed_y = drone.get_speed_y()
            tel.speed_z = drone.get_speed_z()
            tel.acc_x = drone.get_acceleration_x()
            tel.acc_y = drone.get_acceleration_y()
            tel.acc_z = drone.get_acceleration_z()
            tel.temp = drone.get_temperature()
            tel.height = drone.get_height()
            tel.tof_dist = drone.get_distance_tof()
            tel.abs_height = drone.get_barometer()
            tel.battery = drone.get_battery()
            tel.flight_time = drone.get_flight_time()
            tel.speedp, tel.turnp = mm.get_drone_speed()
            
            # VIEW/CAMERA
            frame = drone.get_frame_read().frame
            view.get_view(frame, tel)
            # this is mega blocking, need to fix before face detection
            # def view_loop():
            #     while True:
            #         view.get_view(frame, tel)
            
            # global is_viewing
            # if is_viewing == False:
            #     view_thread = threading.Thread(target=view_loop)
            #     view_thread.start()
            #     is_viewing = True

            # view.get_view(frame, tel)

            # AUX ACTIONS

            # takeoff and landing
            if takeoff == 1 and not flying:
                # blocking action, needs own thread
                takeoff_thread = threading.Thread(target=drone.takeoff)
                takeoff_thread.start()
                flying = True
                #drone.takeoff()

            elif land == 1 and flying:
                landing_thread = threading.Thread(target=drone.land)
                landing_thread.start()
                flying = False
                #drone.land()
            
            # backflip
            if bf == 1 and flying:
                try:
                    backflip_thread = threading.Thread(target=drone.flip_back)
                    backflip_thread.start()
                    #drone.flip_back()
                except:
                    print("Backflip not available.")
            
            # exit
            if ex == 1:
                drone.end()
                flying = False
                raise Exception("Flight ending...")
            
            if swpcam == 1:
                if camera_dir == tello.Tello.CAMERA_FORWARD:
                    drone.set_video_direction(tello.Tello.CAMERA_DOWNWARD)
                    camera_dir = tello.Tello.CAMERA_DOWNWARD

                elif camera_dir == tello.Tello.CAMERA_DOWNWARD:
                    drone.set_video_direction(tello.Tello.CAMERA_FORWARD)
                    camera_dir = tello.Tello.CAMERA_FORWARD

            # RC ACTION
            drone.send_rc_control(lr, fb, ud, rot)
        
        if testing:
            #pass
            print(lr, fb, ud, rot)

        time.sleep(0.05)




if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print("Exiting drone...")
        print(e)