
from pynput import keyboard

class MultikeyListener:
    """Get keys that are being pressed simultaneously.
    Does not support special characters as in pynput:
    only characters who has a corresponding pynput.keyboard.KeyCode,
    and not those with a pynput.keyboard.Key (enter, space, ctrl, etc).
    """
    def __init__(self):
        self.keys_pressed = []
        self.listening = False
        self.listener = keyboard.Listener(
            on_press = self.on_press, 
            on_release = self.on_release
            )
    
    def on_press(self, key):
        """Called on key press.
        """
        try:
            if key.char not in self.keys_pressed:
                self.keys_pressed.append(key.char)

        except AttributeError:
            print(f"{key} has no char value")
    
    def on_release(self, key):
        """Called on key release.
        """
        try:
            if key.char in self.keys_pressed:
                self.keys_pressed.remove(key.char)
        except AttributeError:
            print(f"{key} has no char value")
    
    def get_pressed(self):
        """Returns a list of the keys currently being pressed.
        """
        if not self.listening:
            self.keys_pressed = []
            print("Listener is off")

        return self.keys_pressed
    
    def start_listener(self):
        """Starts the keyboard listener thread.
        """
        if self.listening:
            print("Listener is already on")
        else:
            self.listener.start()
            self.listening = True
    
    def stop_listener(self):
        """Joins the keyboard listener thread.
        """
        if not self.listening:
            print("Listener is already off")
        else:
            self.listener.join()
            self.listening = False
