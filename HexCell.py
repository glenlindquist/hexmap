import random
from pygame.math import *
from HexMetrics import *
from HexCoordinates import *

class HexCell(object):
    
    def __init__(self, x, y):
        self.position = Vector2(x, y)
        self.neighbors = []
        self.chunk = 0
        self.coordinates = HexCoordinates().from_position((self.position))
        self.type = 0 # determines grass, desert, water, etc
        self.colors = self.generate_colors(self.type)

    def change_type(self, new_type):
        self.type = new_type
        self.colors = self.generate_colors(new_type)
        self.chunk.enabled = True
        self.chunk.changed = True

    def generate_colors(self, type):
        if type == 0:
            return [
                (random.randint(20, 100), 120, random.randint(20, 100)),
                (random.randint(20, 100), 120, random.randint(20, 100)),
                (random.randint(20, 100), 120, random.randint(20, 100)),
                (random.randint(20, 100), 120, random.randint(20, 100)),
                (random.randint(20, 100), 120, random.randint(20, 100)),
                (random.randint(20, 100), 120, random.randint(20, 100))
            ]
        elif type == 1:
            return [
                (random.randint(20, 100), random.randint(20, 100), 120),
                (random.randint(20, 100), random.randint(20, 100), 120),
                (random.randint(20, 100), random.randint(20, 100), 120),
                (random.randint(20, 100), random.randint(20, 100), 120),
                (random.randint(20, 100), random.randint(20, 100), 120),
                (random.randint(20, 100), random.randint(20, 100), 120)
            ]
        elif type == 2:
            return [
                (random.randint(20, 100), 120, random.randint(20, 100)),
                (random.randint(20, 100), 120, random.randint(20, 100)),
                (random.randint(20, 100), 120, random.randint(20, 100)),
                (random.randint(20, 100), 120, random.randint(20, 100)),
                (random.randint(20, 100), 120, random.randint(20, 100)),
                (random.randint(20, 100), 120, random.randint(20, 100))
            ]
        elif type == 3:
            return [
                (random.randint(20, 100), 120, random.randint(20, 100)),
                (random.randint(20, 100), 120, random.randint(20, 100)),
                (random.randint(20, 100), 120, random.randint(20, 100)),
                (random.randint(20, 100), 120, random.randint(20, 100)),
                (random.randint(20, 100), 120, random.randint(20, 100)),
                (random.randint(20, 100), 120, random.randint(20, 100))
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
