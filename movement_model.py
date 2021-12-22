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
    "k" : "takeoff",
    "f" : "backflip",
    "2" : "speedup",
    "1" : "speeddown",
    "3" : "turndown",
    "4" : "turnup",
    "0" : "exit",
    "t" : "swapcam"
    }

drone_speed = 80 # 0-100 cm/s
turn_rate = 100
kh.start_listening()

def get_movement_actions():
    actions = []
    for key_input in kh.get_pressed():
        if key_input in KEY_MAPPINGS.keys():
            actions.append(KEY_MAPPINGS[key_input])
    return actions

def get_rc_output_vector(actions):
    vector = [0, 0, 0, 0]
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
            vector[3] = -turn_rate
        elif action == "rotateright":
            vector[3] = turn_rate
        
        global drone_speed
        global turn_rate

        # change speed
        if action == "speeddown":
            drone_speed -= 1
        elif action == "speedup":
            drone_speed += 1
        
        if action == "turndown":
            turn_rate -= 1
        elif action == "turnup":
            turn_rate += 1

    return vector[0], vector[1], vector[2], vector[3]


def get_aux_action_vector(actions):
        vector = [0, 0, 0, 0, 0]
        for action in actions:
            
            # land/takeoff
            if action == "takeoff":
                vector[0] = 1
            elif action == "land":
                vector[1] = 1

            if action == "backflip":
                vector[2] = 1
            
            if action == "exit":
                vector[3] = 1

            if action == "swapcam":
                vector[4] = 1
        
        return vector[0], vector[1], vector[2], vector[3], vector[4]

def get_drone_speed():
    global drone_speed, turn_rate
    return drone_speed, turn_rate
            