import pygame
# Colors
BLUE = "#01399D"
GOLD = "#FAD315"
PINK = "#E15A97"
POWDER = "#A9CCF4"
SEASHELL = "#FBF3F0"
GREEN = "#32CD32"
ORANGE = "#FF8C00"
SATO = "#b3795f"

def hex_to_rgb(hex):
    return tuple(int(hex[1+i:1+i+2], 16) for i in (0, 2, 4))

SATO_RGB = hex_to_rgb(SATO)
BLUE_RGB = hex_to_rgb(BLUE)
GOLD_RGB = hex_to_rgb(GOLD)
PINK_RGB = hex_to_rgb(PINK)
POWDER_RGB = hex_to_rgb(POWDER)
SEASHELL_RGB = hex_to_rgb(SEASHELL)
GREEN_RGB = hex_to_rgb(GREEN)
ORANGE_RGB = hex_to_rgb(ORANGE)
