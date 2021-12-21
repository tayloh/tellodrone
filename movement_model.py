"""
model for the drones movement based on keyboard input
"""

import keyboard_handler as kh

KEY_MAPPINGS = {
    "w" : "forward",
    "s" : "backward",
    "a" : "left",
    "d" : "right",
    "q" : "rotateleft",
    "e" : "rotateright",
    "o" : "up",
    "p" : "down",
    "l" : "land",
    "k" : "takeoff"
    }

drone_speed = 20 # 0-100 cm/s
kh.start_listening()

def get_movement_actions():
    actions = []
    for key_input in kh.get_pressed():
        if key_input in KEY_MAPPINGS.keys():
            actions.append(KEY_MAPPINGS[key_input])
    return actions

def get_rc_output_vector(actions):
    vector = [0, 0, 0, 0, 0]
    for action in actions:

        # forward/back
        if action == "forward":
            vector[1] = drone_speed
        elif action == "backward":
            vector[1] = -drone_speed

        # left/right
        if action == "left":
            vector[0] = -drone_speed
        elif action == "right":
            vector[0] = drone_speed
        
        # up/down
        if action == "up":
            vector[2] = drone_speed
        elif action == "down":
            vector[2] = -drone_speed
        
        # rot left/right
        if action == "rotateleft":
            vector[3] = -drone_speed
        elif action == "rotateright":
            vector[3] = drone_speed
        
        # land/takeoff
        if action == "takeoff":
            vector[4] = 1
        elif action == "land":
            vector[4] = 2
    
    return vector[0], vector[1], vector[2], vector[3], vector[4]

def set_drone_speed(speed):
    global drone_speed
    drone_speed = speed

def get_drone_speed():
    return drone_speed
            