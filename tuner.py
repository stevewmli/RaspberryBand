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
    sleep(0.1)


def main():
    # turner adjustment
    rpi = pigpio.pi()
    l_turner = 2
    l_drummer = 3

    r_turner = 14
    r_drummer = 15

    r2_turner = 27
    r2_drummer = 17

    l2_turner = 23
    l2_drummer = 24

    rpi.set_PWM_frequency(l_turner, 50)
    rpi.set_PWM_frequency(l_drummer, 50)
    rpi.set_PWM_frequency(r_turner, 50)
    rpi.set_PWM_frequency(r_drummer, 50)

    rpi.set_PWM_frequency(l2_turner, 50)
    rpi.set_PWM_frequency(l2_drummer, 50)
    rpi.set_PWM_frequency(r2_turner, 50)
    rpi.set_PWM_frequency(r2_drummer, 50)

    rpi.set_servo_pulsewidth(l_turner, 1800)
    rpi.set_servo_pulsewidth(l_drummer, 1500)
    rpi.set_servo_pulsewidth(r_turner, 1500)
    rpi.set_servo_pulsewidth(r_drummer, 1500)

    rpi.set_servo_pulsewidth(l2_turner, 1800)
    rpi.set_servo_pulsewidth(l2_drummer, 1500)
    rpi.set_servo_pulsewidth(r2_turner, 1500)
    rpi.set_servo_pulsewidth(r2_drummer, 1500)

    sleep(0.3)

    play(rpi, l2_turner, l2_drummer, 2000)  # G5
    play(rpi, l2_turner, l2_drummer, 1930)  # G#5
    play(rpi, l2_turner, l2_drummer, 1860)  # A5
    play(rpi, l2_turner, l2_drummer, 1790)  # A#5
    play(rpi, l2_turner, l2_drummer, 1720)  # B5
    play(rpi, l2_turner, l2_drummer, 1650)  # C6
    play(rpi, l2_turner, l2_drummer, 1570)  # C#6
    rpi.set_servo_pulsewidth(l2_turner, 1790)

    play(rpi, r2_turner, r2_drummer, 1690) # D6
    play(rpi, r2_turner, r2_drummer, 1600) # D#6
    play(rpi, r2_turner, r2_drummer, 1515) # E6
    play(rpi, r2_turner, r2_drummer, 1435) # F6
    play(rpi, r2_turner, r2_drummer, 1350) # F#6
    play(rpi, r2_turner, r2_drummer, 1260) # G6
    rpi.set_servo_pulsewidth(r2_turner, 1515)

    play(rpi, l_turner, l_drummer, 1995)  # G#6
    play(rpi, l_turner, l_drummer, 1915)  # A6
    play(rpi, l_turner, l_drummer, 1855)  # A#6
    play(rpi, l_turner, l_drummer, 1790)  # B6
    play(rpi, l_turner, l_drummer, 1730)  # C7
    play(rpi, l_turner, l_drummer, 1660)  # C#7
    play(rpi, l_turner, l_drummer, 1600)  # D7
    rpi.set_servo_pulsewidth(l_turner, 1810)

    play(rpi, r_turner, r_drummer, 1730) # D#7
    play(rpi, r_turner, r_drummer, 1640) # E7
    play(rpi, r_turner, r_drummer, 1575) # F7
    play(rpi, r_turner, r_drummer, 1510) # F#7
    play(rpi, r_turner, r_drummer, 1440) # G7
    play(rpi, r_turner, r_drummer, 1380) # G#7
    play(rpi, r_turner, r_drummer, 1290) # A7
    rpi.set_servo_pulsewidth(r_turner, 1500)




if __name__ == "__main__":
    main()
