
# Colors
BLUE = "#01399D"
GOLD = "#FAD315"
PINK = "#E15A97"
POWDER = "#A9CCF4"
SEASHELL = "#FBF3F0"

def hex_to_rgb(hex):
    return tuple(int(hex[1+i:1+i+2], 16) for i in (0, 2, 4))


BLUE_RGB = hex_to_rgb(BLUE)
GOLD_RGB = hex_to_rgb(GOLD)
PINK_RGB = hex_to_rgb(PINK)
POWDER_RGB = hex_to_rgb(POWDER)
SEASHELL_RGB = hex_to_rgb(SEASHELL)