from time import sleep
import math
import numpy
import json

try:
    import pigpio
    force_virtual_mode = False
except ModuleNotFoundError:
    print("pigpio not installed, running in test mode")
    force_virtual_mode = True

import tqdm

class ServoConfig:
    def __init__(self, center_pw, center_angle, range, angle_pws, degree_ms):
        self.center_pw = center_pw
        self.center_angle = center_angle
        self.range = range
        self.angle_pws = angle_pws
        self.degree_ms = degree_ms


class Player:
    def __init__(self, rpi, num_of_notes, turner, drummer, turner_config, drummer_config):
        self.rpi = rpi
        self.num_of_notes = num_of_notes
        self.angle_btw_notes = (turner_config.range[1] - turner_config.range[0]) / (num_of_notes - 1)
        self.turner = turner
        self.drummer = drummer
        self.turner_config = turner_config
        self.drummer_config = drummer_config

        # the pulse frequency should be no higher than 100Hz - higher values could (supposedly) damage the servos
        self.rpi.set_PWM_frequency(turner, 50)
        self.rpi.set_PWM_frequency(drummer, 50)

        # initialize servo position
        self.rpi.set_servo_pulsewidth(turner, self.angles_to_pw(turner_config, 90))
        self.rpi.set_servo_pulsewidth(drummer, self.angles_to_pw(drummer_config, 90))

    def angles_to_pw(self, servo_config, angle):
        if servo_config.angle_pws:
            servo_array = numpy.array(servo_config.angle_pws)
            return numpy.poly1d(
                numpy.polyfit(
                    servo_array[:,0],
                    servo_array[:,1],
                    3
                )
            )

        else:
            return self.naive_angles_to_pulse_widths(servo_config, angle)

    def naive_angles_to_pulse_widths(self, servo_config, angle):
        result = (angle - servo_config.center_angle) * servo_config.degree_ms + servo_config.center_pw
        print(result)
        return result
        

    def play_note(self, note_id, turn_wait):
        # turn to the correct note
        start_angle = self.turner_config.range[0]
        target_angle = start_angle + self.angle_btw_notes * note_id
        
        self.angles_to_pw(self.turner_config, target_angle)

        # hit the note
        self.rpi.set_servo_pulsewidth(self.turner, 
                                      self.angles_to_pw(self.turner_config, target_angle))
        sleep(turn_wait)
        self.rpi.set_servo_pulsewidth(self.drummer, 
                                      self.angles_to_pw(self.drummer_config, 30))
        sleep(0.1)
        self.rpi.set_servo_pulsewidth(self.drummer, 
                                      self.angles_to_pw(self.drummer_config, 90))


class RaspberryBand:
    def __init__(self):
        # instantiate this Raspberry Pi as a pigpio.pi() instance
        self.rpi = pigpio.pi()

        self.players = []
        self.players.append(Player(self.rpi, 7, 2, 3, 
                                 ServoConfig(1500, 90, [68.0, 112.0], None, 10), 
                                 ServoConfig(1500, 90, [30.0, 150.0], None, 10)))

        # by default we use a wait factor of 0.1 for accuracy
        # self.wait = wait or .1


def main():
    # read yaml configuration
    # register player


    # band = RaspberryBand()
    # band.players[0].play_note(0, 0.5)
    # band.players[0].play_note(0, 0.2)
    # band.players[0].play_note(1, 0.2)
    # band.players[0].play_note(1, 0.2)
    # band.players[0].play_note(2, 0.2)
    # band.players[0].play_note(3, 0.2)
    # band.players[0].play_note(4, 0.2)
    # band.players[0].play_note(5, 0.2)
    # band.players[0].play_note(5, 0.5)
    # band.players[0].play_note(4, 0.3)
    # band.players[0].play_note(3, 0.4)
    # band.players[0].play_note(5, 0.2)
    # band.players[0].play_note(3, 0.2)
    # band.players[0].play_note(5, 0.2)
    # band.players[0].play_note(3, 0.2)

    # band.players[0].play_note(4, 0.5)
    # band.players[0].play_note(3, 0.2)
    # band.players[0].play_note(2, 0.4)
    # band.players[0].play_note(2, 0.2)
    # band.players[0].play_note(3, 0.2)
    # band.players[0].play_note(4, 0.2)
    # band.players[0].play_note(2, 0.2)

    # band.players[0].play_note(3, 0.5)
    # band.players[0].play_note(2, 0.2)
    # band.players[0].play_note(1, 0.4)
    # band.players[0].play_note(3, 0.2)
    # band.players[0].play_note(1, 0.2)
    # band.players[0].play_note(3, 0.2)
    # band.players[0].play_note(1, 0.2)

    # band.players[0].play_note(2, 0.5)
    # band.players[0].play_note(1, 0.2)
    # band.players[0].play_note(0, 0.4)
    # band.players[0].play_note(0, 0.2)
    # band.players[0].play_note(1, 0.2)
    # band.players[0].play_note(2, 0.2)
    # band.players[0].play_note(0, 0.2)



if __name__ == "__main__":
    main()