from time import sleep

class Percussionist:
    def __init__(self, rpi, notes, turner, drummer):
        self.rpi = rpi
        self.notes = notes
        self.turner = turner
        self.drummer = drummer
        self.drummer_up = 1500

        # frequency in Hz 50 Hz = 20ms
        self.rpi.set_PWM_frequency(turner, 50)
        self.rpi.set_PWM_frequency(drummer, 50)   # frequency in Hz

        self.rpi.set_servo_pulsewidth(turner, 1500)
        sleep(0.1)
        self.rpi.set_servo_pulsewidth(drummer, self.drummer_up)
        sleep(0.1)

    def play_node(self, note, len):
        if note == 'Sleep':
            sleep(len)
            return

        pw = self.notes[note]
        self.rpi.set_servo_pulsewidth(self.turner, pw)
        sleep(0.1)

        self.rpi.set_servo_pulsewidth(self.drummer, 1300)
        sleep(0.1)
        self.rpi.set_servo_pulsewidth(self.drummer, self.drummer_up)
        sleep(len)