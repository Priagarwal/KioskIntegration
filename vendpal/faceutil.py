import cv2
import numpy as np

# cascade = cv2.CascadeClassifier('lbpcascade_frontalface.xml')
# cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
cascade = cv2.CascadeClassifier('haarcascade_frontalface_alt.xml')
# cascade = cv2.CascadeClassifier('haarcascade_frontalface_alt2.xml')

def largest_face(img):
    try:
        return max(faces(img), key=lambda (face, x,y,w,h): w*h)
    except ValueError:
        return np.empty(shape=(0,0)), None,None,None,None

def faces(img):
    contrast_img = cv2.equalizeHist(img)
    return [(img[y:y+h, x:x+w], x,y,w,h) for (x,y,w,h) in cascade.detectMultiScale(contrast_img)]
