from time import sleep
import math
import numpy
import json
import tqdm
import sys

try:
    import pigpio
    force_virtual_mode = False
except ModuleNotFoundError:
    print("pigpio not installed, running in test mode")
    force_virtual_mode = True


class Xylophone:
    def __init__(self, rpi, notes, turner, drummer):
        self.rpi = rpi
        self.notes = notes
        self.turner = turner
        self.drummer = drummer
        self.drummer_up = 1420

        # frequency in Hz 50 Hz = 20ms
        self.rpi.set_PWM_frequency(turner, 50)
        self.rpi.set_PWM_frequency(drummer, 50)   # frequency in Hz

        self.rpi.set_servo_pulsewidth(turner, 1500)
        sleep(0.1)
        self.rpi.set_servo_pulsewidth(drummer, self.drummer_up)
        sleep(0.1)

    def play_node(self, note, len):
        pw = self.notes[note]
        self.rpi.set_servo_pulsewidth(self.turner, pw)
        sleep(0.1)

        self.rpi.set_servo_pulsewidth(self.drummer, 1300)
        sleep(0.1)
        self.rpi.set_servo_pulsewidth(self.drummer, self.drummer_up)
        sleep(len)


def main():
    # turner adjustment
    rpi = pigpio.pi()
    notes = {
        "C1": 1700,
        "D1": 1640,
        "E1": 1560,
        "F1": 1500,
        "G1": 1435,
        "A1": 1360,
        "B1": 1300,
        "C2": 1230,
    }

    xp = Xylophone(rpi, notes, 2, 3)
    xp.play_node("C1", 0.5)
    xp.play_node("D1", 0.2)
    xp.play_node("E1", 0.4)
    xp.play_node("C1", 0.2)
    xp.play_node("E1", 0.4)
    xp.play_node("C1", 0.2)
    xp.play_node("E1", 0.6)

    xp.play_node("D1", 0.5)
    xp.play_node("E1", 0.2)
    xp.play_node("F1", 0.2)
    xp.play_node("F1", 0.2)
    xp.play_node("E1", 0.2)
    xp.play_node("D1", 0.2)
    xp.play_node("F1", 0.6)

    xp.play_node("E1", 0.5)
    xp.play_node("F1", 0.2)
    xp.play_node("G1", 0.4)
    xp.play_node("E1", 0.2)
    xp.play_node("G1", 0.4)
    xp.play_node("E1", 0.2)
    xp.play_node("G1", 0.6)

    xp.play_node("F1", 0.5)
    xp.play_node("G1", 0.2)
    xp.play_node("A1", 0.2)
    xp.play_node("A1", 0.2)
    xp.play_node("G1", 0.2)
    xp.play_node("F1", 0.2)
    xp.play_node("A1", 0.6)

    xp.play_node("G1", 0.5)
    xp.play_node("C1", 0.2)
    xp.play_node("D1", 0.2)
    xp.play_node("E1", 0.2)
    xp.play_node("F1", 0.2)
    xp.play_node("G1", 0.2)
    xp.play_node("A1", 0.6)

    xp.play_node("A1", 0.5)
    xp.play_node("D1", 0.2)
    xp.play_node("E1", 0.2)
    xp.play_node("F1", 0.2)
    xp.play_node("G1", 0.2)
    xp.play_node("A1", 0.2)
    xp.play_node("B1", 0.6)

    xp.play_node("B1", 0.5)
    xp.play_node("E1", 0.2)
    xp.play_node("F1", 0.2)
    xp.play_node("G1", 0.2)
    xp.play_node("A1", 0.2)
    xp.play_node("B1", 0.2)
    xp.play_node("C2", 0.6)

    xp.play_node("C2", 0.2)
    xp.play_node("B1", 0.2)
    xp.play_node("A1", 0.5)
    xp.play_node("F1", 0.5)
    xp.play_node("B1", 0.5)
    xp.play_node("G1", 0.5)
    xp.play_node("C2", 0.5)
    xp.play_node("G1", 0.5)
    xp.play_node("C2", 0.5)


def park():
    rpi = pigpio.pi()
    Xylophone(rpi, {}, 2, 3)

if __name__ == "__main__":
    if len(sys.argv) == 2 and sys.argv[1] == "p":
        park()
    else:
        main()
