# Remote Control for DJI Tello drone
Current version with the tkinter gui has a very delayed view.
<br/>
<br/>
* Control DJI Tello drone via keyboard input
* Remote view of front camera view
* Face detection

<br/>

## Dependencies:
* tkinter
* cv2
* pynput
* numpy
* djitellopy

## How to run:
* Run `git clone`
* cd into directory
* Make sure your drone has the latest firmware
* Connect to your drone via wifi
* Run `python main.py`

## Controls:
* w - Forward
* s - Backward
* a - Left
* d - Right
* q - Rotate Left
* e - Rotate Right
* o - Up
* p - Down
* l - Land
* t - Takeoff
* f - Backflip (unreliable)
* 1 - Speed Down
* 2 - Speed Up
* 3 - Turn rate Down
* 4 - Turn rate Up