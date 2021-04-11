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


def move_ahead(player, already_moved, note):
    rkey = player.name + "_right"
    lkey = player.name + "_left"
    if not already_moved[rkey] and player.can_play_right_hand(note):
        already_moved[rkey] = True
        player.move_right_hand(note)
    elif not already_moved[lkey] and player.can_play_left_hand(note):
        already_moved[lkey] = True
        player.move_left_hand(note)

def who_play(xp1, xp2, note):
    if xp1.can_play_right_hand(note):
        return "xp1_right"
    elif xp1.can_play_left_hand(note):
        return "xp1_left"
    if xp2.can_play_right_hand(note):
        return "xp2_right"
    if xp2.can_play_left_hand(note):
        return "xp2_left"
    return ""

def lookahead(instructions, current, note, octave, xp1, xp2):
    # look ahead next five instruction
    index = instructions.index(current)
    next_set = instructions[(index+1):(index+5)]

    
    already_moved = {
        "xp1_right": False,
        "xp1_left": False,
        "xp2_right": False,
        "xp2_left": False,
    }
    
    hand = who_play(xp1, xp2, note)
    if hand != "":
        already_moved[hand] = True

    # start move to the positions
    for n in next_set:
        if n[0] != "note":
            continue

        note = octave_adj(n[1], octave)
        if xp1.can_play_note(note):
            move_ahead(xp1, already_moved, note)
        elif xp2.can_play_note(note):
            move_ahead(xp2, already_moved, note)

    if not already_moved["xp1_right"]:
        xp1.stand_by_right_hand()
    if not already_moved["xp1_left"]:
        xp1.stand_by_left_hand()
    if not already_moved["xp2_right"]:
        xp2.stand_by_right_hand()
    if not already_moved["xp2_left"]:
        xp2.stand_by_left_hand()


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
        "E6":  1525,
        "F6":  1465,
        "F#6": 1405,
        "Gb6": 1405,
        "G6":  1325,
        "G#6":  1245,
        "Ab6":  1245,
        "A6":  1135,
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

    xp1 = Percussionist("xp1", lh, rh)
    xp2 = Percussionist("xp2", lh2, rh2)

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
                # from the current note, find the next note to play

                note = octave_adj(n[1], octave)
                # lookahead(instructions, n, note, octave, xp1, xp2)
                t = timing(n[2], tempos, quarter_per_min)
                print(f"play {note} - #{n[2]}: {t}")

                if xp1.can_play_note(note):
                    # xp2.stand_by()
                    xp1.play_note(note, t)
                elif xp2.can_play_note(note):
                    # xp1.stand_by()
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
