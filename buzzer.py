from pyfirmata import Arduino, util
import numpy as np
from playsound import playsound
import time

class Buzzer:

    def __init__(self, sig_pin, out_pin, analog_pin, board, name=""):
        self.sig_pin = sig_pin # Bascule entre lumiere=0 analog=1
        self.out_pin = out_pin # Alimentation du buzzer
        self.analog_pin = analog_pin
        self.board = board
        self.name = name
        self.buzzer_is_on = True
        self.light_is_on = False
        board.analog[self.analog_pin].enable_reporting()


    def get_analog_value(self):
        if not self.buzzer_is_on:
            print(f"Buzzer off {self.name}")
            return 0
        if self.light_is_on:
            print(f"Buzzer light on {self.name}")
            return 0
        return self.board.analog[self.analog_pin].read()
    
    def turn_on_buzzer(self, value=True):
        self.buzzer_is_on = value
        self.board.digital[self.out_pin] = int(value)
        light = self.light_is_on and not value
        self.light_is_on = light
        self.board.digital[self.out_pin] = int(light)

    def turn_on_light(self, value=True):
        self.light_is_on = value
        self.board.digital[self.out_pin] = int(value)
    


        

class SuperArduino:
    def __init__(self, port="/dev/ttyACM0"):
        self.port = port
        self.board = Arduino(port)
        self.list_buzzer = [
            Buzzer(4+i, 8+i, 0+i, self.board, f"buzzer {i}") \
                for i in range(4) 
        ]
        it = util.Iterator(self.board)
        it.start()
        
    def get_value(self, turn_on=True):
        if turn_on:
            for i in range(4):
                buzzer = self.list_buzzer[i]
                buzzer.turn_on_buzzer()

        liste = [self.list_buzzer[i].get_analog_value() for i in range(4)]
        return liste

    def turn_on_buzzer(self, liste=[True, True, True, True]):
        for i in range(4):
            self.list_buzzer[i].turn_on_buzzer(liste[i])

    def turn_on_light(self, liste=[True, True, True, True]):
        for i in range(4):
            self.list_buzzer[i].turn_on_light(liste[i])

    def get_winner(self, turn_on=True, play_sound=True):
        liste = self.get_value(turn_on)
        if max(liste) < 0.5:
            return None
        else:
            if play_sound:
                playsound('sounds/buzzer1.wav', block=False)
            return np.argmax(liste)

        

