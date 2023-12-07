import pygame
import pygame.gfxdraw
from constants import *
from buzzer import SuperArduino

# Initialize Pygame
pygame.init()
#super_arduino = SuperArduino()
#super_arduino.get_winner() # None ou valeur entre 0 et 3, si buzzer quelconque éteint alors get_winner() va les rallumer, et pour éviter ca on peut faire turn_on = False en paramètre de get_winner()
# Si on veut pas qu'il emmmete de son on peut faire play_sound = False en paramètre de get_winner()                                    
