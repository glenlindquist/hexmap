from pygame.math import *
from hex_metrics import *
from hex_coordinates import *

class Player(object):
    def __init__(self, position = Vector2(0,0)):
        self.position = Vector2(position.x, position.y)
        self.coordinates = []
        self.chunk = HexCoordinates().from_position(self.position)
