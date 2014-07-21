import cv2
import numpy as np

class Capturer:

    def __init__(self, device=0, width=0, height=0):
        self.vc = cv2.VideoCapture(device)
        if width or height:
            self.vc.set(cv2.cv.CV_CAP_PROP_FRAME_WIDTH, width)
            self.vc.set(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT, height)
        else:
            width = self.vc.get(cv2.cv.CV_CAP_PROP_FRAME_WIDTH)
            height = self.vc.get(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT)
        self.color = np.zeros(shape=(height, width, 3), dtype=np.uint8)
        self.gray = cv2.cvtColor(self.color, code=cv2.COLOR_BGR2GRAY)

    def read(self, skip=0):
        self.vc.read(self.color)
        for _ in xrange(skip):
            self.vc.read(self.color)
        cv2.cvtColor(self.color, code=cv2.COLOR_BGR2GRAY, dst=self.gray)


import faceutil
import requests
if __name__ == '__main__':
    capturer = Capturer()
    cv2.namedWindow("preview")
    while True:
        key = cv2.waitKey(1000)
        if key == 27:
            break
        capturer.read(skip=8)
        cv2.imwrite("capture.jpg", capturer.gray)
        with open("capture.jpg", "rb") as img:
            print(requests.post("http://0.0.0.0:5000/recognize", files={"capture.jpg": img}).text)
        face, x,y,w,h = faceutil.largest_face(capturer.gray)
        if face.size:
            cv2.rectangle(capturer.color, (x,y), (x+w, y+h), (255, 255, 255))
        cv2.imshow("preview", capturer.color)
    cv2.destroyAllWindows()
