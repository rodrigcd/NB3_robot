import os
import sys
import struct
import time
import numpy as np

PROJECT_PATH = os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(PROJECT_PATH)

from control.control_with_ps4j import ArduinoCommunicator, ArduinoLightController
from TD_robot.n_step_Sarsa import NStepSarsa


class LearningRobot(ArduinoLightController):

    def __init__(self, interface, learning_class: NStepSarsa, connecting_using_ds4drv=False):
        super().__init__(interface=interface, connecting_using_ds4drv=connecting_using_ds4drv)
        self.learning_class = learning_class
        self.learning_class.save_Q_values()
        self._possible_robot_actions()
        self.arduino.write(b's')

    def _possible_robot_actions(self):
        self.actions = []  # 0: rest, 1: forward, 2: backward
        action_str = "ofb"
        for left_motor in range(3):
            for right_motor in range(3):
                self.actions.append((action_str[left_motor]+action_str[right_motor]))
        print("Available actions", self.actions)

    def on_square_press(self):
        # Start first epoch
        print("Run one epoch")
        operations = self.learning_class.run_epoch()
        for action in operations["Actions"]:
            #byte_string = self.actions[action].encode()
            byte_string = str(action).encode()
            self.arduino.write(byte_string)
            time.sleep(0.5)
        self.arduino.write(b'0')
        time.sleep(0.5)
        print("Wait for reward")
        self.arduino.write(b'led')

    def on_up_arrow_press(self):
        print("Who is a good boy?")
        self.learning_class.receive_feedback(1)
        self.learning_class.update_Q_values()
        self.learning_class._update_epsilon()
        self.print_current_best_actions()
        self.arduino.write(b'led')

    def on_down_arrow_press(self):
        print("Bad robot!")
        self.learning_class.receive_feedback(-1)
        self.learning_class.update_Q_values()
        self.learning_class._update_epsilon()
        self.print_current_best_actions()
        self.arduino.write(b'led')

    def on_left_arrow_press(self):
        print("Mee")
        self.arduino.write(b'led')

    def on_right_arrow_press(self):
        print("Mee")
        self.arduino.write(b'led')

    def on_playstation_button_press(self):
        print("Saving Q values")
        self.learning_class.save_Q_values()

    def on_share_press(self):
        print("Loading Q values")
        self.learning_class.load_Q_values()

    def on_circle_press(self):
        print("Stop!")
        self.arduino.write(b'oo')

    def print_current_best_actions(self):
        Q = self.learning_class.get_Q_values()
        print(Q)
        for i, action in enumerate(self.actions):
            print("State:", action, "Best action:", self.actions[np.argmax(Q[i, :])])

if __name__ == "__main__":
    learning_function = NStepSarsa(n_states=9, n_actions=9, n_steps=10)
    controller = LearningRobot(interface="/dev/input/js0", connecting_using_ds4drv=False, learning_class=learning_function)
    controller.listen()






