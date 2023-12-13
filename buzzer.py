from pyfirmata import Arduino, util
import numpy as np
"from playsound import playsound"
from pygame import mixer
import time, pygame

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
        self.board.digital[self.out_pin].write(int(value))
        light = self.light_is_on and not value
        self.light_is_on = light
        self.board.digital[self.sig_pin].write(int(light))

    def turn_on_light(self, value=True):
        print(f"Turn on light {self.name}")
        self.light_is_on = value
        self.board.digital[self.sig_pin].write(int(value))
    


        

class SuperArduino:
    def __init__(self, port="/dev/ttyACM0"):
        self.port = port
        self.board = Arduino(port)
        it = util.Iterator(self.board)
        it.start()        
        self.list_buzzer = [
            Buzzer(4,  8, 0, self.board, f"Buzzer {0}"),
            Buzzer(5,  9, 1, self.board, f"Buzzer {1}"),
            Buzzer(6, 11, 2, self.board, f"Buzzer {2}"),
            Buzzer(7, 10, 3, self.board, f"Buzzer {3}")
        ]
        mixer.init()
        mixer.music.load("sounds/buzzer_bip_qpuc.wav")

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
        if max(liste) < 0.4:
            return None
        else:
            if play_sound:
                mixer.music.play()
            return np.argmax(liste)

        


        

class ShadowSuperArduino:
    def __init__(self, port="/dev/ttyACM0"):
        self.on = [True, True, True, True]
        mixer.init()
        mixer.music.load("sounds/buzzer_bip_qpuc.wav")

    def get_value(self, turn_on=True):
        return [True]*4

    def turn_on_buzzer(self, liste=[True, True, True, True]):
        self.on = liste

    def turn_on_light(self, liste=[True, True, True, True]):
        pass

    def get_winner(self, turn_on=True, play_sound=True):
        def play_sound():
            if play_sound:
                mixer.music.play()
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_j and self.on[0]:
                    play_sound()
                    return 0
                if event.key == pygame.K_k and self.on[1]:
                    play_sound()
                    return 1
                if event.key == pygame.K_l and self.on[2]:
                    play_sound()
                    return 2
                if event.key == pygame.K_m and self.on[3]:
                    play_sound()
                    return 3
                    
        return None

        

