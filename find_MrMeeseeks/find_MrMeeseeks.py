import os
import sys

PROJECT_PATH = os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(PROJECT_PATH)

import numpy as np
import cv2
import time

from control.control_with_ps4j import ArduinoCommunicator

class RaspiCam(object):

    def __init__(self, window_name='robot_view'):
        self.window_name = window_name
        self.capture = cv2.VideoCapture(0)
        cv2.namedWindow(window_name)
        self.update_frame()
        self.image_center = np.array((self.capture.get(cv2.CAP_PROP_FRAME_HEIGHT), self.capture.get(cv2.CAP_PROP_FRAME_WIDTH)))/2
        self.image_center = np.flip(self.image_center)

    def update_frame(self):
        ret, frame = self.capture.read()
        self.frame = cv2.rotate(frame, cv2.ROTATE_180)

    def show_video(self):
        while True:
            self.update_frame()
            cv2.imshow(self.window_name, self.frame)
            cv2.waitKey(1)

class FindMrMeeseeks(RaspiCam):

    def __init__(self, window_name='robot_view'):
        super().__init__(window_name)

    def estimate_position_from_image(self, frame):
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        mr_color = hsv[220:260, 300:340, :]
        # print(hsv.shape, mr_color)
        normalization_val = 255/100
        h_norm = 255/360

        # Body detection
        low_color = np.array([int(135*h_norm), int(3*normalization_val), int(3*normalization_val)])
        high_color = np.array([int(145*h_norm), int(100*normalization_val), int(70*normalization_val)])
        frame_mask = cv2.inRange(hsv, low_color, high_color)
        only_color_frame = cv2.bitwise_and(frame, frame, mask=frame_mask)
        kernel = np.ones((30,30),np.float32)/(30*30)
        soft_mask = cv2.filter2D(frame_mask,-1,kernel)
        mr_meeseks_pos = np.unravel_index(np.argmax(soft_mask, axis=None), soft_mask.shape)
        mr_meeseks_pos = np.flip(mr_meeseks_pos)
        # Eye detectio
        #low_color = np.array([int(0*h_norm), int(10*normalization_val), int(0*normalization_val)])
        #high_color = np.array([int(360*h_norm), int(100*normalization_val), int(10*normalization_val)])
        #hair_frame_mask = cv2.inRange(hsv, low_color, high_color)
        #hair_only_color_frame = cv2.bitwise_and(frame, frame, mask=frame_mask)
        return only_color_frame, soft_mask, mr_meeseks_pos

    def show_video(self):
        while True:
            self.update_frame()
            only_color_frame, frame_mask, pos = self.estimate_position_from_image(self.frame)
            self.frame = cv2.circle(self.frame, tuple(pos), 30, (0, 0, 255), 5)
            cv2.imshow(self.window_name, self.frame)
            cv2.imshow("mask", frame_mask)
            cv2.waitKey(1)

    def find(self, buffer_size=10, signal_size=15):
        self.arduino = ArduinoCommunicator()

        time.sleep(1)
        position_buffer = []
        last_pos = self.image_center
        for i in range(buffer_size):
            only_color_frame, frame_mask, pos = self.estimate_position_from_image(self.frame)
            position_buffer.append(pos)
            last_pos = last_pos*0.9 + pos*0.1

        while True:
            self.update_frame()
            only_color_frame, frame_mask, pos = self.estimate_position_from_image(self.frame)
            position_buffer.pop(0)
            position_buffer.append(pos)
            last_pos = last_pos*0.9 + pos*0.1
            self.frame = cv2.circle(self.frame, tuple((last_pos).astype(np.int)), 30, (0, 0, 255), 5)
            self.frame = cv2.circle(self.frame, tuple(self.image_center.astype(np.int)), 30, (255, 0, 0), 5)
            cv2.imshow(self.window_name, self.frame)
            cv2.waitKey(1)

            dif = last_pos-self.image_center
            if dif[0] > 80:
                for i in range(signal_size*2):
                    self.arduino.write(b'rig')
                print("turn right", dif[0])
            elif dif[0] < -80:
                for i in range(signal_size):
                    self.arduino.write(b'lef')
                print("turn left", dif[0])
            else:
                for i in range(signal_size*5):
                    self.arduino.write(b'for')
            self.arduino.write(b'res')

if __name__ == "__main__":
    camera = FindMrMeeseeks()
    camera.find()
