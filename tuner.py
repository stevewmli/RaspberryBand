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

    rpi.set_servo_pulsewidth(drummer, 1370)
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

    play(rpi, turner, drummer, 2015) # G5
    play(rpi, turner, drummer, 1920) # G#5
    play(rpi, turner, drummer, 1855) # A5
    play(rpi, turner, drummer, 1770) # A#6
    play(rpi, turner, drummer, 1670) # B5
    play(rpi, turner, drummer, 1580) # C6

    play(rpi, turner, drummer, 1380) # C#6
    play(rpi, turner, drummer, 1305) # D6
    play(rpi, turner, drummer, 1230) # D#6
    play(rpi, turner, drummer, 1160) # E6
    play(rpi, turner, drummer, 1080) # F6
    play(rpi, turner, drummer, 1010) # F#6
    play(rpi, turner, drummer, 940) # G6
if __name__ == "__main__":
    main()
