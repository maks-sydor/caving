class Tile:
    def __init__(self, walkable=True, damage=0, color="black"):
        self.walkable = walkable
        self.damage = damage
        self.color = color

    def __str__(self):
        return f"Tile: walkable: {self.walkable}, damage: {self.damage}, color: {self.color}"

    def __eq__(self, o: object) -> bool:
        return super().__eq__(o)
