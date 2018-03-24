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
        self.colors = [
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
