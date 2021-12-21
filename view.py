"""
graphical user interface
"""

import cv2 as cv
import vision

info = []

def get_view(frame):
    global info
    for i, text in enumerate(info):
        cv.putText(frame, text, (30,(i+1) * 30), cv.FONT_HERSHEY_PLAIN, 
        1, (0, 255, 0), 1, cv.LINE_AA)

    cv.imshow("drone", frame)
    info = []
    cv.waitKey(1)

def set_info_text(text):
    info.append(text)