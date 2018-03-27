from pygame.math import *
from hex_metrics import *

class HexCoordinates(object):
    def __init__(self, x = 0, z = 0):
        self.x = int(x)
        self.z = int(z)
        self.y = int(-x - z)

    def __str__(self):
        return "(" + str(self.x) + "," + str(self.y) + "," + str(self.z) + ")"

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y and self.z == other.z

    def from_offset_coordinates(self, x, y):
        return HexCoordinates(x - y / 2, y)
    
    def from_position(self, position):
        x = position.x / (HexMetrics.inner_radius * 2.0)
        y = -x
        offset = position.y / (HexMetrics.outer_radius * 3.0)
        x -= offset
        y -= offset
        iX = round(x)
        iY = round(y)
        iZ = round(-x - y)
        
        if (iX + iY + iZ) != 0:
            dX = abs(x - iX)
            dY = abs(y - iY)
            dZ = abs(-x - y - iZ)
            
            if dX > dY and dX > dZ:
                iX = -iY - iZ
            elif dZ > dY:
                iZ = -iX - iY
        
        return HexCoordinates(iX, iZ)
    
    def to_position(self):
        position = Vector2(0,0)
        position.y = self.z * (HexMetrics.outer_radius * 1.5)
        position.x = (self.x + (position.y / (HexMetrics.outer_radius * 3))) * (HexMetrics.inner_radius * 2)
        return position

    def chunk_coords_containing_pos(self, position):
        """Given a position, returns the coordinates of the chunk that contains that position"""
        coordinates = self.from_position(position)
        z_coordinate = coordinates.z - (coordinates.z % HexMetrics.chunk_size_y)
        x_coordinate = (
            (coordinates.x + (coordinates.z / 2))
            - ((coordinates.x + (coordinates.z / 2)) % HexMetrics.chunk_size_x)
            - (z_coordinate / 2)
        )
        return HexCoordinates(x_coordinate, z_coordinate)

    def chunk_pos_containing_pos(self, position):
        return self.chunk_coords_containing_pos(position).to_position()