import serial
import time

# Source: https://www.instructables.com/id/Arduino-Python-Communication-via-USB/
def arduino_to_python():
    arduino = serial.Serial('/dev/ttyUSB0', 9600, timeout=.1)
    while True:
        data = arduino.readline()[:-2] #the last bit gets rid of the new-line chars
        if data:
            print(data)

# Source https://create.arduino.cc/projecthub/Jalal_Mansoori/python3-and-arduino-communication-c33192
def python_to_arduino():
    arduino=serial.Serial('/dev/ttyUSB0', 9600)
    time.sleep(2)

    print("Enter 1 to turn ON LED and 0 to turn OFF LED")

    while True:
        
        datafromUser=input()
        if datafromUser == '1':
            arduino.write(b'1')
            print("LED  turned ON")
        elif datafromUser == '0':
            arduino.write(b'0')
            print("LED turned OFF")

if __name__ == "__main__":
    python_to_arduino()
