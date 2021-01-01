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
         "G#6": 2020,
         "A6":  1940,
         "A#6": 1870,
         "B6":  1810,
         "C7":  1740,
         "C#7": 1690,
         "D7": 1600,
    }

    r_notes = {
         "D#7": 1740,
         "E7": 1660,
         "F7": 1560,
         "F#7": 1500,
         "G7": 1430,
         "G#7": 1360,
         "A7": 1290,
    }

    lh = Hand(rpi, l_notes, "B6", 2, 3)
    rh = Hand(rpi, r_notes, "F#7", 14, 15)

    xp = Percussionist(lh, rh)
    with open(song) as f:
        notes = yaml.load(f, Loader=yaml.FullLoader)
        for n in notes:
            xp.play_note(n[0], n[1])

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
