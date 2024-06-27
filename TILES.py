"""
Contains a list of Tile objects for the game, as well as some functions,
such as get tile by humidity or get a random tile
"""

import random

from Tile import Tile
from COLORS import *


# Entities
player = Tile(color=light)
dead_player = Tile(color=dark)
enemy = Tile(walkable=False, damage=1, color=red)

# Blocks
shallow_lava = Tile(walkable=True, damage=1, color=light_orange)
lava = Tile(walkable=True, damage=3, color=orange)
deep_lava = Tile(walkable=True, damage=5, color=dark_orange)

shallow_water = Tile(walkable=True, damage=-1, color=light_blue)
water = Tile(walkable=True, damage=-2, color=blue)
deep_water = Tile(walkable=True, damage=-3, color=dark_blue)

trampled_grass = Tile(walkable=True, color=light_green)
grass = Tile(walkable=True, color=green)
high_grass = Tile(walkable=True, color=dark_green)

soft_rock = Tile(walkable=False, color=light_gray)
rock = Tile(walkable=False, color=gray)
hard_rock = Tile(walkable=False, color=dark_gray)

darkness = Tile(walkable=False, color=dark)

# Items
chest = Tile(walkable=True, color=light_yellow)  # Can contain a VRI or a pickaxe
pickaxe = Tile(walkable=True, color=red)
vri = Tile(walkable=True, color=dark_blue)  # VRI - Vision Range Increase


# Sorted by temperature - highest to lowest
ground_tiles = [deep_lava, deep_lava, lava, lava, lava, shallow_lava, shallow_lava,
                hard_rock, rock, soft_rock,
                trampled_grass, grass, high_grass,
                shallow_water, water, water, water, water, deep_water, deep_water]

lake_biome = [high_grass, grass, grass, trampled_grass, shallow_water, water, water, deep_water, deep_water, deep_water]

# Tiles that have a chance of generating a chest
chest_tiles = [trampled_grass, grass, high_grass]

# Tiles that can and need to be mined with a pickaxe
need_pickaxe = [soft_rock, rock, hard_rock]

# Tiles where the player can spawn
spawn_tiles = [trampled_grass, grass, high_grass, shallow_water, water, deep_water]


def random_tile(allowed_tiles=ground_tiles):
    return allowed_tiles[random.randint(0, len(allowed_tiles) - 1)]


def get_tile(temp, manual=False, tile_list=ground_tiles):
    """
    Get a tile by temperature

    :param temp: -1 to 1
    :param manual: Auto-calculate tile or not
    :param tile_list: The list from which the tiles will be taken
    :return: one of the tiles (string)
    """

    normalized_temp = (temp + 1) / 2  # -1 to 1 maps to 0 to 1

    if manual:
        if normalized_temp > 0.65: return water
        elif normalized_temp > 0.5: return grass
        elif normalized_temp > 0.35: return rock
        else: return lava
    else:
        # Uncomment this for the lake_biome:
        # if normalized_temp > 0.6:
        #     return deep_water
        # elif normalized_temp < 0.25:
        #     return high_grass
        index = round(normalized_temp * (len(tile_list)-1))
        return tile_list[index]
