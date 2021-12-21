"""
keyboard handler that tracks multiple key presses at the same time
"""

from pynput import keyboard as kb

class ListenerNotActiveError(Exception):
    """
    When an action requires the listener but listening = False
    """
    pass

class UnidentifiedReleaseError(Exception):
    """
    When a key that was never pressed gets released
    """
    pass 

keys_pressed = []
listening = False

def on_press(key):
    """
    on_press event
    """
    if key == kb.Key.esc:
        global listening
        listening = False
        return False
    
    try:
        if key.char not in keys_pressed:
            keys_pressed.append(key.char)
    except AttributeError:
        print(f'{key} has no char value')    

def on_release(key):
    """
    on_release event
    """
    try:
        if key.char in keys_pressed:
            keys_pressed.remove(key.char)
        else:
            raise UnidentifiedReleaseError("Unidentified key release", key)
    except AttributeError:
        print(f'{key} has no char value')

def get_pressed():
    """
    Gets all pressed keys
    """
    if not listening:
        raise ListenerNotActiveError("Keyboard listener is not running")

    return keys_pressed

def is_pressed(key):
    """
    Checks if a certain key is pressed
    """
    if not listening:
        raise ListenerNotActiveError("Keyboard listener is not running")

    try:
        if key.char in keys_pressed:
            return True
        else:
            return False  
    except:
        print(f'{key} has no char value')
        return False

#listener = kb.Listener(on_press=on_press, on_release=on_release)
#listener.start()
#listening = True

def start_listening():
    """
    Starts listener thread
    """
    global listener
    listener = kb.Listener(on_press=on_press, on_release=on_release)
    listener.start()

    global listening
    listening = True

def stop_listening():
    """
    Stops listener thread
    """
    global listener
    listener.join()
    
    global listening
    listening = False

    