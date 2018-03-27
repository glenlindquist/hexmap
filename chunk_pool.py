from hex_chunk import *


class ChunkPool(object):
    POOL_SIZE = 15
    pool = []

    def __init__(self):
        for i in range(self.POOL_SIZE):
            self.pool.append(HexChunk(Vector2(0, 0)))

    def take_from_pool(self, position):
        chunk = self.pool.pop()
        chunk.position = position
        chunk.coordinates = HexCoordinates().from_position(chunk.position)
        return chunk

    def return_to_pool(self, chunk):
        chunk.clear()
        self.pool.append(chunk)