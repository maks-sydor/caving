import STYLES
from Map import Map
from Vector2 import Vector2
from TILES import *


class Player:
    def __init__(self, terrain_map):
        """
        A player class that moves across the terrain_map.

        :param terrain_map: The map that the player uses to move
        """

        self.terrain_map = terrain_map
        # Explored map is fully dark in the beginning (we don't know anything yet)
        self.explored_map = Map(terrain_map.rows, terrain_map.columns)

        self.has_pickaxe = False
        self.pickaxe_power = 0
        self.exploring_radius = 4
        self.max_health = 20
        self.health = self.max_health
        self.dead = False

        self.chests_opened_on_level = 0

        self.pos = Vector2(0, 0)
        self.spawn()

    def move(self, amount):
        """
        Moves the player by set amount and interacts with tiles.
        Throws a TypeError if the amount isn't whole (float, double...)

        :param amount: Vector2, by how much do we move. INT ONLY.
        """

        # First of all, we can't fo anything if we are dead
        if self.dead:
            return

        # The player can't move by float, so check it
        if not isinstance(amount.x, int) or not isinstance(amount.y, int):
            raise TypeError("The player can only move by an integer amount, as there can't be \"float\" tiles")

        # Check if the position is valid
        new_pos = self.pos + amount

        # If we are not MORE than the edges
        if not new_pos.x >= self.terrain_map.columns and not new_pos.y >= self.terrain_map.rows:
            # And if we are not LESS that the edges
            if not new_pos.x < 0 and not new_pos.y < 0:
                # Get the tile at the position that we want to walk to
                tile = self.terrain_map.map[new_pos.x][new_pos.y]

                # Walk on it if it is walkable
                if tile.walkable:
                    self.damage(tile.damage)

                    # But if it is a chest
                    if tile == chest:
                        # Open it
                        print(STYLES.BLUE + "You opened a chest!" + STYLES.RESET)
                        self.terrain_map.map[new_pos.x][new_pos.y] = grass
                        self.chests_opened_on_level += 1
                        if self.chests_opened_on_level == 5:
                            print(STYLES.WHITE + STYLES.ITALIC + STYLES.BALD +
                                  "You found all the chests on this level!" + STYLES.RESET)
                            self.chests_opened_on_level = 0

                        chance = random.randint(1, 3)
                        if chance == 1:
                            print(STYLES.BLUE + "You found a pickaxe!" + STYLES.RESET)
                            # Get a pickaxe
                            self.terrain_map.map[new_pos.x][new_pos.y] = pickaxe
                        elif chance == 2:
                            print(STYLES.BLUE + "You found a VRI!" + STYLES.RESET)
                            # Get a VRI
                            self.terrain_map.map[new_pos.x][new_pos.y] = vri
                        else:
                            print(STYLES.BLUE + "It was empty." + STYLES.RESET)

                    # But if it isn't a chest
                    else:
                        # Move to it
                        self.pos = new_pos

                        if tile == pickaxe:
                            if not self.has_pickaxe:
                                print(STYLES.CYAN + "You picked up: pickaxe. Now you can mine!" + STYLES.RESET)
                            else:
                                print(STYLES.CYAN + "You picked up: pickaxe." + STYLES.RESET)
                            # And, if it's a pickaxe, pick it up
                            self.terrain_map.map[new_pos.x][new_pos.y] = trampled_grass
                            self.has_pickaxe = True
                            self.pickaxe_power += 1
                            if self.pickaxe_power == 2:
                                print(STYLES.CYAN + f"Your pickaxe power is now {self.pickaxe_power}."
                                                    f" Now you can mine faster!" + STYLES.RESET)
                            if self.pickaxe_power == 3:
                                print(STYLES.CYAN + f"Your pickaxe power is now {self.pickaxe_power}."
                                                    f" Now you can mine 3x3!" + STYLES.RESET)
                            else:
                                print(STYLES.CYAN + f"Your pickaxe power is now {self.pickaxe_power}."
                                                    f" Find more pickaxes to increase it." + STYLES.RESET)
                        if tile == vri:
                            if self.exploring_radius == 1:
                                print(STYLES.CYAN + "You picked up: VRI. Now you can see farther!" + STYLES.RESET)

                            self.terrain_map.map[new_pos.x][new_pos.y] = trampled_grass
                            self.exploring_radius += 1
                            print(STYLES.CYAN + f"Your current seeing radius: {self.exploring_radius}" + STYLES.RESET)

                # If we have a pickaxe and the tile is rock, mine it
                elif self.has_pickaxe:
                    if self.pickaxe_power == 1:
                        if tile == soft_rock:
                            # Soft rock: mine it and move there
                            self.terrain_map.map[new_pos.x][new_pos.y] = grass
                            self.pos = new_pos
                        elif tile == rock:
                            # Regular rock: mine it
                            self.terrain_map.map[new_pos.x][new_pos.y] = grass
                        elif tile == hard_rock:
                            # Hard rock: weaken it (turn it into regular rock), but don't mine it
                            self.terrain_map.map[new_pos.x][new_pos.y] = rock
                    if self.pickaxe_power == 2:
                        if tile == soft_rock:
                            # Soft rock: mine it and move there
                            self.terrain_map.map[new_pos.x][new_pos.y] = grass
                            self.pos = new_pos
                        elif tile == rock:
                            # Regular rock: mine it
                            self.terrain_map.map[new_pos.x][new_pos.y] = grass
                            self.pos = new_pos
                        elif tile == hard_rock:
                            # Hard rock: weaken it (turn it into regular rock), but don't mine it
                            self.terrain_map.map[new_pos.x][new_pos.y] = grass
                    elif self.pickaxe_power >= 3:
                        # All the tiles around the mined one
                        original_tile = self.terrain_map.map[new_pos.x][new_pos.y]

                        if original_tile in need_pickaxe:
                            self.terrain_map.map[new_pos.x][new_pos.y] = grass
                            self.pos = new_pos

                        for i in range(-1, 2):
                            for j in range(-1, 2):
                                tile = self.terrain_map.map[new_pos.x + i][new_pos.y + j]
                                if tile in need_pickaxe:
                                    self.terrain_map.map[new_pos.x + i][new_pos.y + j] = grass

                elif not self.has_pickaxe and tile in need_pickaxe:
                    print(STYLES.LIGHT_GRAY + STYLES.ITALIC + "You need to find a pickaxe to mine!" + STYLES.RESET)

                # Explore the area that we've (maybe) just moved to
                self.explore(self.pos)

    def explore(self, position):
        """
        Explores the map at the position

        :param position: around which position do we "look at tiles"
        """

        # For all tiles
        for i in range(self.terrain_map.rows):
            for j in range(self.terrain_map.columns):
                # Calculate the distance to the player
                tile_pos = Vector2(i, j)
                sqr_dist = (position - tile_pos).sqr_magnitude()

                # If it is in our "FOV", write it to our explored map
                if sqr_dist <= self.exploring_radius * self.exploring_radius:
                    self.explored_map.map[i][j] = self.terrain_map.map[i][j]

    def damage(self, amount):
        # Take some health off
        self.health -= amount

        # Die if you ran out of health
        if self.health <= 0:
            self.health = 0
            self.die()
        # And cap the health if you have too much of it
        if self.health > self.max_health:
            self.health = self.max_health

        if amount > 0:
            if self.dead:
                print(STYLES.RED + STYLES.BALD + f"You took {amount} damage and died! "
                                                 f"Press \"N\" to start a new game." + STYLES.RESET)
            else:
                print(STYLES.RED + f"You took {amount} damage! Health: {self.health}" + STYLES.RESET)
        elif amount < 0:
            print(STYLES.GREEN + f"You healed {abs(amount)} hp! Health: {self.health}" + STYLES.RESET)

    def die(self):
        self.dead = True

    def interact(self, position):
        pass

    def set_terrain_map(self, new_terrain_map):
        self.terrain_map = new_terrain_map

    def spawn(self, position=None):
        """
        Spawns the player at this position and forgets the map.

        :param position: The position where the player is spawned. Is changed if the player spawns inside a block
        """

        if position is None:
            self.pos = Vector2(int(self.terrain_map.rows / 2), int(self.terrain_map.columns / 2))
        else:
            self.pos = position

        self.dead = False
        self.health = self.max_health

        # Move the player to the right if the tile that it spawned on isn't walkable
        tile = self.terrain_map.map[self.pos.x][self.pos.y]
        if tile not in spawn_tiles:
            while tile not in spawn_tiles:
                self.pos.x += 1
                tile = self.terrain_map.map[self.pos.x][self.pos.y]

        # Reset the explored map
        self.explored_map = Map(self.terrain_map.rows, self.terrain_map.columns)

        # Explore the part where the player is standing
        self.explore(self.pos)
