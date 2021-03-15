from time import sleep
import tqdm
import sys
import yaml
import re
from percussionist import Percussionist, Hand

try:
    import pigpio
    force_virtual_mode = False
except ModuleNotFoundError:
    print("pigpio not installed, running in test mode")
    force_virtual_mode = True

def octave_adj(note, adj):
    nums = re.findall(r'\d+', note)
    src = nums[0]
    tgt = int(src) + adj
    return note.replace(src, str(tgt))
    
def timing(tempo, tempos, quarter_per_min):
    sec_per_quarter = 60.0 / quarter_per_min
    t = tempo.replace(".", "")
    scale = tempos[t]
    dot_scale = 1.5 if ("." in tempo) else 1.0
    return sec_per_quarter * scale * dot_scale

def main(song):
    # turner adjustment
    rpi = pigpio.pi()

    tempos = {
        "thirty_second": 0.125,
        "sixteenth": 0.25,
        "eighth": 0.5,
        "quarter": 1.0,
        "half": 2.0,
        "whole": 4.0,
        "double_whole": 8.0
    }

    l_notes = {
        "G5":  1825,
        "G#5": 1760,
        "Ab5": 1760,
        "A5":  1695,
        "A#5": 1630,
        "Bb5": 1630,
        "B5":  1555,
        "C6":  1480,
        "C#6": 1410,
        "Db6": 1410,
        "D6": 1340,
    }

    r_notes = {
        "D#6": 1605,
        "Eb6": 1605,
        "E6":  1520,
        "F6":  1455,
        "F#6": 1390,
        "Gb6": 1390,
        "G6":  1305,
        "G#6":  1230,
        "Ab6":  1230,
        "A6":  1140,
    }

    l2_notes = {
        "A#6": 1820,
        "Bb6": 1820,
        "B6":  1755,
        "C7":  1690,
        "C#7": 1625,
        "Db7": 1625,
        "D7":  1550,
        "D#7": 1490,
        "Eb7": 1490,
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

    quarter_per_min = 90.0
    octave = 0

    with open(song) as f:
        instructions = yaml.load(f, Loader=yaml.FullLoader)

        for n in instructions:
            if n[0] == "quarter_per_min":
                quarter_per_min = n[1]
                continue

            if n[0] == "octave":
                octave = n[1]
                continue

            if n[0] == "rest":
                t = timing(n[1], tempos, quarter_per_min)
                print(f"rest: #{t}\n")
                sleep(t)
                continue

            if n[0] == "note":
                note = octave_adj(n[1], octave)
                t = timing(n[2], tempos, quarter_per_min)
                print(f"play {note} - #{n[2]}: {t}")
                
                if xp1.can_play_note(note):
                    xp2.stand_by()
                    xp1.play_note(note, t)
                elif xp2.can_play_note(note):
                    xp1.stand_by()
                    xp2.play_note(note, t)
                else:
                    print(f"No player can play {n[1]}: {n[2]}")
                    sleep(t)

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
