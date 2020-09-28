from pyPS4Controller.controller import Controller
import serial
import time

class MyController(Controller):
    # Test function and package from https://github.com/ArturSpirin/pyPS4Controller
    def __init__(self, **kwargs):
        Controller.__init__(self, **kwargs)


class ArduinoLightController(Controller):
    # Just to turn light on an off
    def __init__(self, **kwargs):
        Controller.__init__(self, **kwargs)
        self.arduino = ArduinoCommunicator()

    def on_square_press(self):
        self.arduino.write(b'led')

def ArduinoCommunicator():
    arduino = serial.Serial('/dev/ttyUSB0', 9600)
    time.sleep(2)
    return arduino


class RobotPS4Controller(ArduinoLightController):
    # Light and robot movement
    def __init__(self, **kwargs):
        ArduinoLightController.__init__(self, **kwargs)

    def on_L3_right(self, value):
        self.arduino.write(b'rig')
        print("turn right")

    def on_L3_left(self, value):
        self.arduino.write(b'lef')
        print("turn left")

    def on_L3_up(self, value):
        self.arduino.write(b'for')
        print("move forward")

    def on_L3_down(self, value):
        self.arduino.write(b'bac')
        print("move backwards")

    def on_L3_x_at_rest(self):
        self.arduino.write(b'res')
        print("rest")

    def on_L3_y_at_rest(self):
        self.arduino.write(b'res')
        print("rest")

if __name__ == "__main__":
    controller = RobotPS4Controller(interface="/dev/input/js0", connecting_using_ds4drv=False)
    controller.listen()


