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
         "G5":  2000,
         "G#5": 1930,
         "A5":  1860,
         "A#5": 1790,
         "B5":  1720,
         "C6":  1650,
         "C#6": 1570,
    }

    r_notes = {
         "D6":  1690,
         "D#6": 1600,
         "E6":  1515,
         "F6":  1435,
         "F#6": 1350,
         "G6":  1260,
    }

    l2_notes = {
         "G#6": 1995,
         "A6":  1915,
         "A#6": 1855,
         "B6":  1790,
         "C7":  1730,
         "C#7": 1660,
         "D7":  1600,
    }

    r2_notes = {
         "D#7": 1730,
         "E7":  1640,
         "F7":  1575,
         "F#7": 1510,
         "G7":  1440,
         "G#7": 1380,
         "A7":  1290,
    }

    lh = Hand(rpi, l_notes, "A#5", 23, 24)
    rh = Hand(rpi, r_notes, "E6", 27, 17)

    lh2 = Hand(rpi, l2_notes, "B6", 2, 3)
    rh2 = Hand(rpi, r2_notes, "F#7", 14, 15)

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

    gpios = [2, 3, 14, 15]

    for gpio in gpios:
        rpi.set_PWM_frequency(gpio, 50)
        rpi.set_servo_pulsewidth(gpio, 1500)

if __name__ == "__main__":
    if len(sys.argv) == 2 and sys.argv[1] == "p":
        park()
    else:
        main(sys.argv[1])
