from TILES import *
from perlin_noise import PerlinNoise


class Map:
    def __init__(self, rows=25, columns=25):
        """
        A map of Tiles, rows x columns.

        :param rows: How many rows does the map have
        :param columns: How many columns does the map have
        """

        self.rows = rows
        self.columns = columns
        # The map is filled with darkness at the start
        self.map = [[darkness for _ in range(self.columns)] for _ in range(self.rows)]

    def randomize(self, allowed_tiles=ground_tiles):
        """
        Fills the map with random tiles from the allowed_tiles list

        :param allowed_tiles: Tile[] - default ground_tiles
        """

        for i in range(self.rows):
            for j in range(self.columns):
                self.map[i][j] = random_tile(allowed_tiles)

    def fill(self, tile):
        """
        Fills the map with a set tile. Equivalent to randomize(allowed_tiles=[tile]).

        :param tile: The tile that will be used
        """

        self.randomize(allowed_tiles=[tile])

    def generate(self, seed=None, octaves=7.5):
        """
        Generates a map using perlin noise as a temperature map.

        :param seed: The seed that will be used in terrain and item generation
        :param octaves: The number of octaves for perlin noise
        """

        # Setup
        random.seed(seed)
        noise = PerlinNoise(octaves=octaves, seed=seed)
        xPix, yPix = self.columns, self.rows

        # Create a noise map
        noise = [[noise([i / xPix, j / yPix]) for j in range(xPix)] for i in range(yPix)]

        # Fill the terrain map with tiles from the "ground_tiles" based on the noise map
        for i in range(self.rows):
            for j in range(self.columns):
                self.map[i][j] = get_tile(noise[i][j], tile_list=ground_tiles)

        # Place the chests
        chest_amount = 5
        chest_chance = int((self.rows * self.columns) / chest_amount)

        while chest_amount > 0:
            for i in range(self.rows):
                for j in range(self.columns):
                    tile = self.map[i][j]
                    if tile in chest_tiles:
                        if random.randint(1, chest_chance) == 1:
                            self.map[i][j] = chest
                            chest_amount -= 1
                            if chest_amount == 0:
                                return
