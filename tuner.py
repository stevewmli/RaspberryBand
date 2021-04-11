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

    rpi.set_servo_pulsewidth(drummer, 1300)
    sleep(0.1)
    rpi.set_servo_pulsewidth(drummer, 1500)
    sleep(0.2)


def main():
    # turner adjustment
    rpi = pigpio.pi()
    l_turner = 23       # 1 2
    l_drummer = 24

    r_turner = 17       # 4 3
    r_drummer = 27

    r2_turner = 2       # 5 6
    r2_drummer = 3

    l2_turner = 14      # 7 8
    l2_drummer = 15

    rpi.set_servo_pulsewidth(l_turner, 1630)
    rpi.set_servo_pulsewidth(r_turner, 1405)
    rpi.set_servo_pulsewidth(l2_turner, 1625)
    rpi.set_servo_pulsewidth(r2_turner, 1485)
    sleep(0.5)

    play(rpi, l_turner, l_drummer, 1825)  # G5
    play(rpi, l_turner, l_drummer, 1760)  # G#5
    play(rpi, l_turner, l_drummer, 1695)  # A5
    play(rpi, l_turner, l_drummer, 1630)  # A#5
    play(rpi, l_turner, l_drummer, 1555)  # B5
    play(rpi, l_turner, l_drummer, 1480)  # C6  
    play(rpi, l_turner, l_drummer, 1410)  # C#6  
    play(rpi, l_turner, l_drummer, 1340)  # D6  
    rpi.set_servo_pulsewidth(l_turner, 1630)

    play(rpi, r_turner, r_drummer, 1605) # D#6
    play(rpi, r_turner, r_drummer, 1525) # E6
    play(rpi, r_turner, r_drummer, 1465) # F6
    play(rpi, r_turner, r_drummer, 1405) # F#6
    play(rpi, r_turner, r_drummer, 1325) # G6
    play(rpi, r_turner, r_drummer, 1245) # G#6
    play(rpi, r_turner, r_drummer, 1135) # A6
    rpi.set_servo_pulsewidth(r_turner, 1405)

    play(rpi, l2_turner, l2_drummer, 1820) # A#6
    play(rpi, l2_turner, l2_drummer, 1755) # B6
    play(rpi, l2_turner, l2_drummer, 1690) # C7
    play(rpi, l2_turner, l2_drummer, 1625) # C#7
    play(rpi, l2_turner, l2_drummer, 1550) # D7
    play(rpi, l2_turner, l2_drummer, 1490) # D#7
    play(rpi, l2_turner, l2_drummer, 1420) # E7
    play(rpi, l2_turner, l2_drummer, 1345) # F7
    rpi.set_servo_pulsewidth(l2_turner, 1625)

    play(rpi, r2_turner, r2_drummer, 1630)  # F#7
    play(rpi, r2_turner, r2_drummer, 1555)  # G7
    play(rpi, r2_turner, r2_drummer, 1485)  # G#7
    play(rpi, r2_turner, r2_drummer, 1415)  # A7
    play(rpi, r2_turner, r2_drummer, 1335)  # A#7
    play(rpi, r2_turner, r2_drummer, 1265)  # B7
    play(rpi, r2_turner, r2_drummer, 1175)  # C8
    rpi.set_servo_pulsewidth(r2_turner, 1485)


if __name__ == "__main__":
    main()
