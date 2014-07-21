import cv2

cv2.namedWindow("preview")
vc = cv2.VideoCapture(0)
cascade = cv2.CascadeClassifier('/usr/share/opencv/lbpcascades/lbpcascade_frontalface.xml')

if vc.isOpened(): # try to get the first frame
    rval, frame = vc.read()
else:
    rval = False

if rval:
    grayframe = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    contrastframe = cv2.equalizeHist(grayframe)
    faces = cascade.detectMultiScale(contrastframe, 1.3, 5)
    for (x, y, w, h) in faces:
        cv2.rectangle(grayframe, (x,y), (x+w, y+h), 255, 2)
    cv2.imshow("preview", grayframe)

while rval:
    key = cv2.waitKey(20)
    if key == 27: # exit on ESC
        break
    rval, frame = vc.read(frame)
    cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY, grayframe)
    cv2.equalizeHist(grayframe, contrastframe)
    faces = cascade.detectMultiScale(contrastframe, 1.3, 5)
    for (x, y, w, h) in faces:
        cv2.rectangle(grayframe, (x,y), (x+w, y+h), (255,0,0), 2)
    cv2.imshow("preview", grayframe)
cv2.destroyWindow("preview")
