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

    xp = Percussionist(rpi, notes, 2, 3)
    with open('./songs/do_re_me.yaml') as f:
        notes = yaml.load(f, Loader=yaml.FullLoader)
        for note in notes:
            xp.play_node(notes[0], notes[1])

def park():
    rpi = pigpio.pi()
    Percussionist(rpi, {}, 2, 3)

if __name__ == "__main__":
    if len(sys.argv) == 2 and sys.argv[1] == "p":
        park()
    else:
        main()
