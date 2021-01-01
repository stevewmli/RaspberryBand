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
    sleep(0.1)

    rpi.set_servo_pulsewidth(drummer, 1200)
    sleep(0.1)
    rpi.set_servo_pulsewidth(drummer, 1500)
    sleep(0.3)


def main():
    # turner adjustment
    rpi = pigpio.pi()
    l_turner = 2
    l_drummer = 3

    r_turner = 14
    r_drummer = 15

    rpi.set_PWM_frequency(l_turner, 50)
    rpi.set_PWM_frequency(l_drummer, 50)
    rpi.set_PWM_frequency(r_turner, 50)
    rpi.set_PWM_frequency(r_drummer, 50)

    rpi.set_servo_pulsewidth(l_turner, 1810)
    rpi.set_servo_pulsewidth(l_drummer, 1500)
    rpi.set_servo_pulsewidth(r_turner, 1500)
    rpi.set_servo_pulsewidth(r_drummer, 1500)

    sleep(0.3)

    # play(rpi, turner, drummer, 2015) # G5
    # play(rpi, turner, drummer, 1920) # G#5
    # play(rpi, turner, drummer, 1855) # A5
    # play(rpi, turner, drummer, 1770) # A#6
    # play(rpi, turner, drummer, 1670) # B5
    # play(rpi, turner, drummer, 1580) # C6

    # play(rpi, turner, drummer, 1380) # C#6
    # play(rpi, turner, drummer, 1305) # D6
    # play(rpi, turner, drummer, 1230) # D#6
    # play(rpi, turner, drummer, 1160) # E6
    # play(rpi, turner, drummer, 1080) # F6
    # play(rpi, turner, drummer, 1010) # F#6
    # play(rpi, turner, drummer, 940) # G6

    # play(rpi, turner, drummer, 2060) # G5
    # play(rpi, turner, drummer, 1980) # G5
    # play(rpi, turner, drummer, 1900) # G#5
    # play(rpi, turner, drummer, 1820) # A5
    # play(rpi, turner, drummer, 1740) # A#6
    # play(rpi, turner, drummer, 1660) # B5
    # play(rpi, turner, drummer, 1580) # C6

    # play(rpi, turner, drummer, 1500) # C#6
    # play(rpi, turner, drummer, 1420) # D6
    # play(rpi, turner, drummer, 1340) # D#6
    # play(rpi, turner, drummer, 1260) # E6
    # play(rpi, turner, drummer, 1180) # F6
    # play(rpi, turner, drummer, 1100) # F#6
    # play(rpi, turner, drummer, 1020) # G6

    # RIGHT HAND
    # play(rpi, turner, drummer, 2000) # B6
    # play(rpi, turner, drummer, 1930) # C7
    # play(rpi, turner, drummer, 1875) # C#7
    # play(rpi, turner, drummer, 1805) # D7

    # play(rpi, turner, drummer, 1740) # D#7
    # play(rpi, turner, drummer, 1670) # E7
    # play(rpi, turner, drummer, 1560) # F7
    # play(rpi, turner, drummer, 1500) # F#7
    # play(rpi, turner, drummer, 1430) # G7
    # play(rpi, turner, drummer, 1360) # G#7
    # play(rpi, turner, drummer, 1290) # G#7

    # LEFT HAND
    # play(rpi, l_turner, l_drummer, 2020)  # G#6
    # play(rpi, l_turner, l_drummer, 1940)  # A6
    # play(rpi, l_turner, l_drummer, 1870)  # A#6
    # play(rpi, l_turner, l_drummer, 1810)  # B6
    # play(rpi, l_turner, l_drummer, 1740)  # C7
    # play(rpi, l_turner, l_drummer, 1670)  # C#7
    # play(rpi, l_turner, l_drummer, 1600)  # D7

    # play(rpi, l_turner, l_drummer, 1530)  # D#7
    # play(rpi, l_turner, l_drummer, 1460)  # E7
    # play(rpi, l_turner, l_drummer, 1370)  # F#7
    # play(rpi, l_turner, l_drummer, 1300)  # F#7

    # LEFT HAND
    play(rpi, l_turner, l_drummer, 2020)  # G#6
    play(rpi, l_turner, l_drummer, 1940)  # A6
    play(rpi, l_turner, l_drummer, 1870)  # A#6
    play(rpi, l_turner, l_drummer, 1810)  # B6
    play(rpi, l_turner, l_drummer, 1740)  # C7
    play(rpi, l_turner, l_drummer, 1670)  # C#7
    play(rpi, l_turner, l_drummer, 1600)  # D7
    rpi.set_servo_pulsewidth(l_turner, 1810)

    play(rpi, r_turner, r_drummer, 1740) # D#7
    play(rpi, r_turner, r_drummer, 1660) # E7
    play(rpi, r_turner, r_drummer, 1560) # F7
    play(rpi, r_turner, r_drummer, 1500) # F#7
    play(rpi, r_turner, r_drummer, 1430) # G7
    play(rpi, r_turner, r_drummer, 1360) # G#7
    play(rpi, r_turner, r_drummer, 1290) # A7
    rpi.set_servo_pulsewidth(r_turner, 1500)


if __name__ == "__main__":
    main()
