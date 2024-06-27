from tkinter import *
import copy

import COLORS
import STYLES
from Map import Map
from Player import Player
from Vector2 import Vector2
import TILES

# Map variables
rows, columns = 50, 50
terrain_map = Map(rows, columns)
seed = 8  # Saved seeds: 4
terrain_map.generate(seed)

full_map = Map(rows, columns)

# Player
player = Player(terrain_map)

# Display variables
TILE_SIZE = 15
squares = []

# Window dimensions
WIDTH = TILE_SIZE * columns
HEIGHT = TILE_SIZE * rows

# Window setup
root = Tk()
root.title("Caving")
root.geometry(f"{WIDTH}x{HEIGHT}")

canvas = Canvas(root, width=WIDTH, height=HEIGHT)
canvas.pack()


def update_map():
    """
    Updates the full map to show the explored terrain and the player
    """

    full_map.map = copy.deepcopy(player.explored_map.map)
    player_tile = TILES.dead_player if player.dead else TILES.player
    full_map.map[player.pos.x][player.pos.y] = player_tile


def square(x, y, color):
    return canvas.create_rectangle(x, y, x + TILE_SIZE, y + TILE_SIZE, fill=color, outline="")


def square_with_outline(x, y, inside_color, outside_color, outline_size):
    s_out = canvas.create_rectangle(x, y,
                                    x + TILE_SIZE, y + TILE_SIZE,
                                    fill=outside_color, outline="")
    s_in = canvas.create_rectangle(x + outline_size, y + outline_size,
                                   x + TILE_SIZE - outline_size, y + TILE_SIZE - outline_size,
                                   fill=inside_color, outline="")

    return s_in, s_out


def clear():
    """
    Deletes all the squares from the canvas and clear the list
    :return:
    """
    for s in squares:
        canvas.delete(s)
    squares.clear()


def draw_field():
    """
    Draws the full_map on the screen
    """
    clear()

    # Create a square for each tile with the color of that tile and add it to the list
    for i in range(rows):
        for j in range(columns):
            if full_map.map[i][j] in [TILES.player, TILES.dead_player]:
                x = i * TILE_SIZE
                y = j * TILE_SIZE
                outline = 3

                if player.dead:
                    s_in, s_out = square_with_outline(x, y, COLORS.black, COLORS.darker_gray, outline)
                else:
                    s_in, s_out = square_with_outline(x, y, COLORS.light_gray, COLORS.light, outline)

                squares.append(s_out)
                squares.append(s_in)
            else:
                s = square(i * TILE_SIZE, j * TILE_SIZE, full_map.map[i][j].color)
                squares.append(s)


def handle_input(key):
    # Movement
    if key == "up":
        player.move(Vector2(0, -1))
    elif key == "left":
        player.move(Vector2(-1, 0))
    elif key == "down":
        player.move(Vector2(0, 1))
    elif key == "right":
        player.move(Vector2(1, 0))

    # Reveal the map if the "r" key is pressed
    elif key == "r":
        print(STYLES.WHITE + STYLES.ITALIC + STYLES.BALD + "You now know the layout of this level!" + STYLES.RESET)
        player.explored_map = terrain_map
    # Generate a new map if the "n" key is pressed
    elif key == "n":
        print(STYLES.WHITE + STYLES.ITALIC + STYLES.BALD + "You are now on a new level!" + STYLES.RESET)
        terrain_map.generate()
        player.set_terrain_map(terrain_map)
        player.spawn()
    # Give the player "operator rights" (give him the best pickaxe and heal him) if the "o" key is pressed
    elif key == "o":
        print(STYLES.WHITE + STYLES.ITALIC + STYLES.BALD + "Gave the best pickaxe!" + STYLES.RESET)
        player.has_pickaxe = True
        player.pickaxe_power = 3
        player.health = player.max_health

    update_map()
    draw_field()


def print_welcome_message():
    text = f"""
{STYLES.WHITE}Hi!
{STYLES.BLUE}This is a simple game about caves that I made to learn how to use Perlin Noise.
You can only move and mine, but you can also {STYLES.GREEN}take damage from lava and heal in water.
{STYLES.BLUE}Each "level" contains 5 chests, and each chest has a random item of (empty, pickaxe, VRI).

{STYLES.WHITE}Items:
{STYLES.GREEN}VRI means "Vision Range Increaser".
{STYLES.BLUE}It increases the range at which you can see. Has a dark blue color.
{STYLES.GREEN}Pickaxes increase your pickaxe level.
{STYLES.BLUE}At 0 you can't mine. At 1 you can mine. At 2 you mine faster. And at 3+ you mine 3x3 and with maximum speed. They are red-colored.

{STYLES.WHITE}Blocks:
{STYLES.GREEN}Orange: {STYLES.BLUE}lava, damages you, more if deep, less if shallow.
{STYLES.GREEN}Blue: {STYLES.BLUE}water. Same as lava, heals you differently based on the depth.
{STYLES.GREEN}Green: {STYLES.BLUE}grass. You can walk on it.
{STYLES.GREEN}Gray: {STYLES.BLUE}stone. Mineable if you have a pickaxe.
{STYLES.GREEN}Gold: {STYLES.BLUE}chests. You can walk into them to open them.

{STYLES.WHITE}Controls:
{STYLES.GREEN}Movement: {STYLES.BLUE}WASD or arrow keys to move. You can't move into stone.
{STYLES.GREEN}Mining: {STYLES.BLUE}actually, you can move into stone! You mine it this way (if you have a pickaxe, of course!)
{STYLES.GREEN}Other:{STYLES.BLUE}
    press {STYLES.BALD}"R"{STYLES.RESET}{STYLES.BLUE} to reveal the map,
    press {STYLES.BALD}"O"{STYLES.RESET}{STYLES.BLUE} to give you "operator rights" - basically give you the best pickaxe, and
    press {STYLES.BALD}"N"{STYLES.RESET}{STYLES.BLUE} to go to a new random level. You will keep your pickaxe power and VRI.

And that is all! You can also go to the "Map" class, and set the "tile_list" on line 58 to "lake_biome".
It will change the terrain generation to be a one with islands in the ocean, though you can't do anything there)

{STYLES.GREEN}You can also create your own "biome": {STYLES.BLUE}it's just a list of tiles, from which, based on the perlin noise value,
a tile is taken - if the value is low, the tile is closer to the beginning of the list, and the other way.

Have fun :)



P.S. You may want to look in the console, it says stuff now and then!
        """ + STYLES.RESET

    print(text)


# Show the map initially
update_map()
draw_field()

print_welcome_message()

# Bind the movement keys
root.bind("w", lambda event: handle_input("up"))
root.bind("<Up>", lambda event: handle_input("up"))
root.bind("a", lambda event: handle_input("left"))
root.bind("<Left>", lambda event: handle_input("left"))
root.bind("s", lambda event: handle_input("down"))
root.bind("<Down>", lambda event: handle_input("down"))
root.bind("d", lambda event: handle_input("right"))
root.bind("<Right>", lambda event: handle_input("right"))

# And the reveal map and the new map keys
root.bind("r", lambda event: handle_input("r"))
root.bind("n", lambda event: handle_input("n"))
root.bind("o", lambda event: handle_input("o"))

root.mainloop()
