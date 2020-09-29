import numpy as np
import cv2

window_name = 'robot_view'
capture = cv2.VideoCapture(0)
cv2.namedWindow(window_name)

class RaspiCam(object):

    def __init__(self, capture, window_name='robot_view'):
        self.window_name = window_name
        self.capture = capture
        self.update_frame()

    def update_frame(self):
        ret, frame = self.capture.read()
        self.frame = cv2.rotate(frame, cv2.ROTATE_180)

    def show_video(self):
        while True:
            self.update_frame()
            cv2.imshow(self.window_name, self.frame)
            cv2.waitKey(1)

class FindMrMeeseeks(RaspiCam):

    def __init__(self, capture, window_name='robot_view'):
        super().__init__(capture, window_name)

    def detect_color_blobs(self, frame):
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        mr_color = hsv[220:260, 300:340, :]
        print(hsv.shape, mr_color)
        normalization_val = 255/100
        h_norm = 255/360
        low_color = np.array([int(110*h_norm), int(30*normalization_val), int(50*normalization_val)])
        high_color = np.array([int(150*h_norm), int(100*normalization_val), int(100*normalization_val)])
        frame_mask = cv2.inRange(hsv, low_color, high_color)
        only_color_frame = cv2.bitwise_and(frame, frame, mask=frame_mask)
        return only_color_frame, frame_mask

    def show_video(self):
        while True:
            self.update_frame()
            only_color_frame = self.detect_color_blobs(self.frame)
            cv2.imshow(self.window_name, self.frame)
            cv2.imshow("mask", only_color_frame)
            cv2.waitKey(1)

if __name__ == "__main__":
    camera = FindMrMeeseeks(capture)
    camera.show_video()
