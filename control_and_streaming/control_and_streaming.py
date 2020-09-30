import os
import sys

PROJECT_PATH = os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(PROJECT_PATH)

from control.control_with_ps4j import DigitalRobotPS4Controller
from find_MrMeeseeks.find_MrMeeseeks import 

if __name__ == "__main__":
    controller = DigitalRobotPS4Controller(interface="/dev/input/js0", connecting_using_ds4drv=False)
    controller.listen()
