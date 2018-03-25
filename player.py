from pygame.math import *
from hex_metrics import *
from hex_coordinates import *
from hex_chunk import *

class Player(object):
    def __init__(self, position = Vector2(0,0)):
        self.position = Vector2(position.x, position.y)
        self.coordinates = []
        self.chunk = HexChunk(Vector2(0,0))
