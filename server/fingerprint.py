import time
import busio
import board
import adafruit_fingerprint
from digitalio import DigitalInOut, Direction
import serial

class Fingerprint:
    def __init__(self):
        led = DigitalInOut(board.D13)
        led.direction = Direction.OUTPUT
        uart = serial.Serial("/dev/ttyS0", baudrate=57600, timeout=1)
        self.finger = adafruit_fingerprint.Adafruit_Fingerprint(uart)
    
    def get_patient_id(self):
        while self.finger.get_image() != adafruit_fingerprint.OK:
            pass
        if self.finger.image_2_tz(1) != adafruit_fingerprint.OK:
            return None
        if self.finger.finger_search() != adafruit_fingerprint.OK:
            return None
        return self.finger.finger_id
    
    def register_finger(self, id: int):
        for finger_img in range(1,3):
            while True:
                i = self.finger.get_image()
                if i == adafruit_fingerprint.OK:
                    print("image taken")
                    break
                if i == adafruit_fingerprint.NOFINGER:
                    print("Scanning")
                else:
                    print("Error")
                    return False
            
            i = self.finger.image_2_tz(finger_img)
            if i != adafruit_fingerprint.OK:
                print("Templating failed")
                return False

            if finger_img == 1:
                time.sleep(1)
                while i != adafruit_fingerprint.NOFINGER:
                    i = self.finger.get_image()
        i = self.finger.store_model(id)
        if i == adafruit_fingerprint.OK:
            print("stored")
        else:
            if i == adafruit_fingerprint.BADLOCATION:
                print("Bad storage location")
            elif i == adafruit_fingerprint.FLASHERR:
                print("Flash storage error")
            else:
                print("Other error")
            return False

        print("Register succeed!")
        return True