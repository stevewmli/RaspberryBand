from time import sleep
import tqdm
import sys
import yaml
from percussionist import Percussionist

try:
    import pigpio
    force_virtual_mode = False
except ModuleNotFoundError:
    print("pigpio not installed, running in test mode")
    force_virtual_mode = True

def play(rpi, turner, drummer, pw):
    rpi.set_servo_pulsewidth(turner, pw)
    sleep(0.3)

    rpi.set_servo_pulsewidth(drummer, 1300)
    sleep(0.1)
    rpi.set_servo_pulsewidth(drummer, 1500)
    sleep(0.2)

def main():
    # turner adjustment
    rpi = pigpio.pi()
    turner = 2
    drummer = 3

    rpi.set_PWM_frequency(turner, 50)
    rpi.set_PWM_frequency(drummer, 50)   # frequency in Hz

    rpi.set_servo_pulsewidth(turner, 1500)
    sleep(0.3)

    play(rpi, turner, drummer, 2015) # C1
    play(rpi, turner, drummer, 1925) # C1#
    play(rpi, turner, drummer, 1855) # D1
    play(rpi, turner, drummer, 1770) # D1#
    play(rpi, turner, drummer, 1685) # E1
    play(rpi, turner, drummer, 1590) # F1
    play(rpi, turner, drummer, 1500) # F1#

    play(rpi, turner, drummer, 1390) # G1
    play(rpi, turner, drummer, 1290) # G1#
    play(rpi, turner, drummer, 1220) # A1
    play(rpi, turner, drummer, 1140) # A1#
    play(rpi, turner, drummer, 1070) # B1
    play(rpi, turner, drummer, 990)  # C2


if __name__ == "__main__":
    main()
