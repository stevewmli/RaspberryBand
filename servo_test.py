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
    # notes = {
    #     "C1": 1700,
    #     "D1": 1640,
    #     "E1": 1560,
    #     "F1": 1500,
    #     "G1": 1435,
    #     "A1": 1360,
    #     "B1": 1300,
    #     "C2": 1230,
    # }

    # play(rpi, turner, drummer, 2015) # G5
    # play(rpi, turner, drummer, 1920) # G#5
    # play(rpi, turner, drummer, 1855) # A5
    # play(rpi, turner, drummer, 1770) # A#5
    # play(rpi, turner, drummer, 1670) # B5
    # play(rpi, turner, drummer, 1580) # C6

    # play(rpi, turner, drummer, 1380) # C#6
    # play(rpi, turner, drummer, 1305) # D6
    # play(rpi, turner, drummer, 1230) # D#6
    # play(rpi, turner, drummer, 1160) # E6
    # play(rpi, turner, drummer, 1080) # F6
    # play(rpi, turner, drummer, 1010) # F#6
    # play(rpi, turner, drummer, 940) # G6

    notes = {
         "G5":  2015,
         "G#5": 1920,
         "A5":  1850,
         "A#5": 1770,
         "B5":  1670,
         "C6":  1580,
         "C#6": 1380,
         "D6": 1305,
         "D#6": 1230,
         "E6": 1160,
         "F6": 1080,
         "F#6": 1010,
         "G6": 940,
    }

    xp = Percussionist(rpi, notes, 2, 3)
    with open('./songs/london_bridge.yaml') as f:
        notes = yaml.load(f, Loader=yaml.FullLoader)
        for n in notes:
            xp.play_node(n[0], n[1])

def park():
    rpi = pigpio.pi()
    Percussionist(rpi, {}, 2, 3)

if __name__ == "__main__":
    if len(sys.argv) == 2 and sys.argv[1] == "p":
        park()
    else:
        main()
