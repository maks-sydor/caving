"""
Those are all the styles that I could find. I tried everything from 0-100, if you put more they start cycling.
You can use them like so:
print(BOX + BALD + CYAN + WHITE_BG + "YOUR TEXT")
"""

RESET = "\u001B[0m"

BALD = "\u001B[1m"
ITALIC = "\u001B[3m"
UNDERSCORE = "\u001B[4m"  # Also 21
MIDDLE_SCORE = "\u001B[9m"

BOX = "\u001B[51m"  # Also 52

WHITE = "\u001B[97m"
BLACK = "\u001B[30m"
RED = "\u001B[31m"  # Also 91
GREEN = "\u001B[32m"  # Also 92
YELLOW = "\u001B[33m"  # Also 93
BLUE = "\u001B[34m"  # Also 94
MAGENTA = "\u001B[35m"  # Also 95
CYAN = "\u001B[36m"  # Also 96
LIGHT_GRAY = "\u001B[37m"  # Also 90

WHITE_BG = "\u001B[7m"
BLACK_BG = "\u001B[40m"
RED_BG = "\u001B[41m"
GREEN_BG = "\u001B[42m"
YELLOW_BG = "\u001B[43m"
BLUE_BG = "\u001B[44m"
MAGENTA_BG = "\u001B[45m"
CYAN_BG = "\u001B[46m"
LIGHT_GRAY_BG = "\u001B[47m"  # Also 100
