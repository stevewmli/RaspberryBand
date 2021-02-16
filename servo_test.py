from time import sleep
import tqdm
import sys
import yaml
from percussionist import Percussionist, Hand

try:
    import pigpio
    force_virtual_mode = False
except ModuleNotFoundError:
    print("pigpio not installed, running in test mode")
    force_virtual_mode = True

def main(song):
    # turner adjustment
    rpi = pigpio.pi()

    l_notes = {
         "G5":  1825,
         "G#5": 1760,
         "A5":  1695,
         "A#5": 1630,
         "B5":  1555,
         "C6":  1480,
         "C#6": 1410,
         "D6": 1340,
    }

    r_notes = {
         "D#6": 1625,
         "E6":  1540,
         "F6":  1475,
         "F#6": 1410,
         "G6":  1325,
         "G#6":  1250,
         "A6":  1160,
    }

    l2_notes = {
         "A#6": 1815,
         "B6":  1755,
         "C7":  1690,
         "C#7": 1625,
         "D7":  1550,
         "D#7": 1490,
         "E7":  1420,
         "F7":  1345,
    }

    r2_notes = {
         "F#7": 1630,
         "G7":  1555,
         "G#7": 1485,
         "A7":  1415,
         "A#7":  1335,
         "B7":  1265,
         "C8":  1175,
    }

    lh = Hand(rpi, l_notes, "A#5", 23, 24)
    rh = Hand(rpi, r_notes, "F#6", 17, 27)

    lh2 = Hand(rpi, l2_notes, "C#7", 14, 15)
    rh2 = Hand(rpi, r2_notes, "A7", 2, 3)

    xp1 = Percussionist(lh, rh)
    xp2 = Percussionist(lh2, rh2)
    with open(song) as f:
        notes = yaml.load(f, Loader=yaml.FullLoader)
        for n in notes:
            if n[0] == "Sleep":
                sleep(n[1])
                continue

            if xp1.can_play_note(n[0]): 
                xp2.stand_by()
                xp1.play_note(n[0], n[1])
            elif xp2.can_play_note(n[0]):
                xp1.stand_by()
                xp2.play_note(n[0], n[1])
            else:
                print(f"No player can play {n[0]}: {n[1]}")

def park():
# turner adjustment
    rpi = pigpio.pi()

    gpios = [2, 3, 14, 15, 27, 17, 23, 24]

    for gpio in gpios:
        rpi.set_PWM_frequency(gpio, 50)
        rpi.set_servo_pulsewidth(gpio, 1500)

if __name__ == "__main__":
    if len(sys.argv) == 2 and sys.argv[1] == "p":
        park()
    else:
        main(sys.argv[1])
