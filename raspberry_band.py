from time import sleep
import readchar
import math
import numpy
import json

try:
    import pigpio
    force_virtual_mode = False
except ModuleNotFoundError:
    print("pigpio not installed, running in test mode")
    force_virtual_mode = True

import tqdm

class RaspberryBand:
    def init(
        self,
        servo_1_centre=1500,
        servo_2_centre=1500
    ):
        self.servo_1_centre = servo_1_centre
        self.servo_2_centre = servo_2_centre

        # instantiate this Raspberry Pi as a pigpio.pi() instance
        self.rpi = pigpio.pi()

        # the pulse frequency should be no higher than 100Hz - higher values could (supposedly) damage the servos
        self.rpi.set_PWM_frequency(14, 50)
        self.rpi.set_PWM_frequency(15, 50)

        # Initialise the pantograph with the motors in the centre of their travel
        self.rpi.set_servo_pulsewidth(14, self.angles_to_pw_1(90))
        sleep(0.3)
        self.rpi.set_servo_pulsewidth(15, self.angles_to_pw_2(90))
        sleep(0.3)

        # by default we use a wait factor of 0.1 for accuracy
        self.wait = wait or .1


def main():
    print("Hello World")

if __name__ == "__main__":
    main()