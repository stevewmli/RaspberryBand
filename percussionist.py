from time import sleep

from yaml.tokens import BlockEndToken


class Hand:
    def __init__(self, rpi, notes, stand_by_note, turner, drummer):
        self.rpi = rpi

        self.notes = notes
        self.turner = turner
        self.drummer = drummer
        self.stand_by_note = stand_by_note

        self.drummer_up = 1500

        # frequency in Hz 50 Hz = 20ms
        self.rpi.set_PWM_frequency(turner, 50)
        self.rpi.set_PWM_frequency(drummer, 50)   # frequency in Hz

        self.rpi.set_servo_pulsewidth(turner, 1500)
        sleep(0.1)
        self.rpi.set_servo_pulsewidth(drummer, self.drummer_up)
        sleep(0.1)

    def play_note(self, note, len):
        if note == 'Sleep':
            sleep(len)
            return

        if note in self.notes:
            pw = self.notes[note]
            self.rpi.set_servo_pulsewidth(self.turner, pw)
            sleep(0.15)

            self.rpi.set_servo_pulsewidth(self.drummer, 1000)
            sleep(0.08)
            self.rpi.set_servo_pulsewidth(self.drummer, self.drummer_up)
            sleep(len / 5.0)
            # sleep(len)
        else:
            sleep(len)

    def can_play_note(self, note):
        return note in self.notes

    def stand_by(self):
        pw = self.notes[self.stand_by_note]
        self.rpi.set_servo_pulsewidth(self.turner, pw)


class Percussionist:
    def __init__(self, left_hand, right_hand):
        self.left_hand = left_hand
        self.right_hand = right_hand

    def play_note(self, note, len):
        len = len / 2.0
        if self.left_hand.can_play_note(note):
            self.right_hand.stand_by()
            self.left_hand.play_note(note, len)
        elif self.right_hand.can_play_note(note):
            self.left_hand.stand_by()
            self.right_hand.play_note(note, len)

    def can_play_note(self, note):
        return self.left_hand.can_play_note(note) or self.right_hand.can_play_note(note)

    def stand_by(self):
        self.left_hand.stand_by()
        self.right_hand.stand_by()
