import random
from pygame.math import *
from hex_metrics import *
from hex_coordinates import *


class HexCell(object):
    def __init__(self, x, y):
        self.position = Vector2(x, y)
        self.neighbors = []
        self.chunk = 0
        self.coordinates = HexCoordinates().from_position((self.position))
        self.terrain = 0 # determines grass, desert, water, etc
        self.colors = self.generate_colors(self.terrain)

    def change_terrain(self, new_terrain):
        if new_terrain > 3:
            new_terrain = 0
        self.terrain = new_terrain
        self.colors = self.generate_colors(new_terrain)
        self.chunk.enabled = True
        self.chunk.changed = True

    def generate_colors(self, terrain):
        if terrain == 0:
            return [
                (random.randint(20, 100), 120, random.randint(20, 100)),
                (random.randint(20, 100), 120, random.randint(20, 100)),
                (random.randint(20, 100), 120, random.randint(20, 100)),
                (random.randint(20, 100), 120, random.randint(20, 100)),
                (random.randint(20, 100), 120, random.randint(20, 100)),
                (random.randint(20, 100), 120, random.randint(20, 100))
            ]
        elif terrain == 1:
            return [
                (random.randint(20, 50), random.randint(20, 100), 120),
                (random.randint(20, 50), random.randint(20, 100), 120),
                (random.randint(20, 50), random.randint(20, 100), 120),
                (random.randint(20, 50), random.randint(20, 100), 120),
                (random.randint(20, 50), random.randint(20, 100), 120),
                (random.randint(20, 50), random.randint(20, 100), 120)
            ]
        elif terrain == 2:
            return [
                (random.randint(150, 170), random.randint(120, 140), random.randint(20, 40)),
                (random.randint(150, 170), random.randint(120, 140), random.randint(20, 40)),
                (random.randint(150, 170), random.randint(120, 140), random.randint(20, 40)),
                (random.randint(150, 170), random.randint(120, 140), random.randint(20, 40)),
                (random.randint(150, 170), random.randint(120, 140), random.randint(20, 40)),
                (random.randint(150, 170), random.randint(120, 140), random.randint(20, 40))
            ]
        elif terrain == 3:
            return [
                (random.randint(0, 20), random.randint(0, 20), random.randint(0, 20)),
                (random.randint(0, 20), random.randint(0, 20), random.randint(0, 20)),
                (random.randint(0, 20), random.randint(0, 20), random.randint(0, 20)),
                (random.randint(0, 20), random.randint(0, 20), random.randint(0, 20)),
                (random.randint(0, 20), random.randint(0, 20), random.randint(0, 20)),
                (random.randint(0, 20), random.randint(0, 20), random.randint(0, 20))
            ]
        else:
            return [
                (random.randint(20, 100), 120, random.randint(20, 100)),
                (random.randint(20, 100), 120, random.randint(20, 100)),
                (random.randint(20, 100), 120, random.randint(20, 100)),
                (random.randint(20, 100), 120, random.randint(20, 100)),
                (random.randint(20, 100), 120, random.randint(20, 100)),
                (random.randint(20, 100), 120, random.randint(20, 100))
            ]
    
    def get_neighbor(self, direction):
        return self.neighbors[direction]
        
    def set_neighbor(self, direction, cell):
        self.neighbors[direction] = cell
        cell.neighbors[direction.opposite()] = self
