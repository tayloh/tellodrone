"""
graphical user interface
"""

import cv2 as cv
import vision

green = (0, 255, 0)

def get_view(frame, telemetry):
    result = frame.copy()
    # find people in frame (doesnt work very well tbh)
    # result = vision.haar_detect_bodies(frame)
    # result = vision.hog_detect_bodies(frame)

    # TODO: need to run facial detection on separate thread
    # and keep track of the last found rects and draw them
    # on the main viewing thread
    # result = vision.haar_detect_faces_frontal(frame)
    # result = vision.haar_detect_faces_profile(result)

    # draw gui elements
    result = draw_battery(result, telemetry.battery)

    result = draw_flight_telemetry(result, telemetry)

    # show frame
    cv.imshow("drone", result)
    cv.waitKey(1)

def draw_battery(frame, battery):
    frame_width = frame.shape[1]
    frame_height = frame.shape[0]

    b_maxlength = frame_width // 5
    b_height = 15
    b_length = int((battery / 100) * b_maxlength)
    x_pos = frame_width // 100
    y_pos = frame_height // 20

    cv.putText(frame, str(battery), (x_pos + b_maxlength + 10, y_pos + 14), cv.FONT_HERSHEY_PLAIN,
    1, green, 1, cv.LINE_AA)

    cv.rectangle(frame, (x_pos, y_pos), (x_pos + b_length, y_pos + b_height), green, -1)
    cv.rectangle(frame, (x_pos, y_pos), (x_pos + b_maxlength, y_pos + b_height), green, 2)

    return frame

def draw_flight_telemetry(frame, tel):
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
            cv.FONT_HERSHEY_PLAIN, 1, green, 1, cv.LINE_AA)
    
    return frame

if __name__ == "__main__":
    import telemetry
    tel = telemetry.Telemetry()
    tel.battery = 87
    cap = cv.VideoCapture(0)

    t = 0
    while t < 500:
        succ, img = cap.read()
        get_view(img, tel)
        t+=1
