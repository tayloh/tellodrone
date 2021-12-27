"""
opencv body/face detection, maybe recognition
filters, processing, etc
"""

import cv2 as cv

hog = cv.HOGDescriptor()
hog.setSVMDetector(cv.HOGDescriptor_getDefaultPeopleDetector())

haar_body = cv.CascadeClassifier("haar/haar_cascade_body.xml")
haar_face_frontal = cv.CascadeClassifier("haar/haar_cascade_face.xml")
haar_face_profile = cv.CascadeClassifier("haar/haar_cascade_faceprofile.xml")

def hog_detect_bodies(img):
    """
    is super slow
    """
    global hog

    people, _ = hog.detectMultiScale(
        img, 
        winStride = (5, 5),
        padding = (3, 3),
        scale = 1.08
        )
    
    for x, y, w, h in people:
        cv.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
    
    return img

def haar_detect_bodies(img):
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

    global haar_body
    rects = haar_body.detectMultiScale(gray, scaleFactor = 1.05, minNeighbors = 3)

    for x, y, w, h in rects:
        cv.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
    
    return img

def haar_detect_faces_frontal(img):
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

    global haar_detect_faces_frontal
    rects = haar_face_frontal.detectMultiScale(gray, scaleFactor = 1.05, minNeighbors = 6)

    # for x, y, w, h in rects:
    #     cv.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)

    return rects

def haar_detect_faces_profile(img):
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

    global haar_face_profile
    rects = haar_face_profile.detectMultiScale(gray, scaleFactor = 1.05, minNeighbors = 3)

    for x, y, w, h in rects:
        cv.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
    
    return img
