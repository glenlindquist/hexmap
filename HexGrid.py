from pygame.math import *
from HexCell import *
from HexMetrics import *
from HexChunk import *

class HexGrid(object):
    def __init__(self, chunk_count_x = 1, chunk_count_y = 1):
        self.cells = []
        self.chunks = []
    
        self.chunk_count_x = chunk_count_x
        self.chunk_count_y = chunk_count_y
    
        self.cell_count_x = 0
        self.cell_count_y = 0

        self.chunk_dict = {}


        # self.create_chunks()

    def update(self):
        for chunk in self.chunks:
            if chunk.enabled:
                chunk.update()

    def load_chunks(self, player):
        for offset in HexMetrics().chunk_offsets:
            chunk_position = player.chunk.to_position() + Vector2(offset[0], offset[1])
            if str(chunk_position) not in self.chunk_dict:
                chunk = HexChunk(chunk_position)
                self.chunks.append(chunk)
                self.chunk_dict[str(chunk.coordinates)] = chunk
                self.create_cells(chunk)

    def unload_chunks(self, player):
        chunks_to_remove = list(chunk for chunk in self.chunk_dict if
                                abs(self.chunk_dict[chunk].position.x - player.chunk.to_position().x) > HexMetrics().chunk_width or
                                abs(self.chunk_dict[chunk].position.y - player.chunk.to_position().y) > HexMetrics().chunk_height
                                )
        for chunk in chunks_to_remove:
            self.chunk_dict[chunk].serialize_chunk()
            del self.chunk_dict[chunk]

    def create_chunks(self):
        """if you wanted to create x * y chunks. currently replaced by load_chunks"""
        for y in range(self.chunk_count_y):
            for x in range(self.chunk_count_x):
                self.create_chunk(x, y)

    def create_chunk(self, x, y):
        if HexMetrics().chunk_size_y % 2 == 0:
            chunk = HexChunk(x * HexMetrics().chunk_width, y * HexMetrics().chunk_height)
        else:
            if y % 2 == 0:
                chunk = HexChunk(x * HexMetrics().chunk_width, y * HexMetrics().chunk_height)
            else:
                chunk = HexChunk(x * HexMetrics().chunk_width + HexMetrics().inner_radius,
                                 y * HexMetrics().chunk_height)
        # self.chunk_dict[chunk.coordinates] = chunk
        self.chunks.append(chunk)
        self.create_cells(chunk)

    def create_cells(self, chunk):
        for y in range(HexMetrics().chunk_size_y):
            for x in range(HexMetrics().chunk_size_x):
                self.create_cell(x, y, chunk)
    
    def create_cell(self, x, y, chunk):
        cell_position = Vector2(0,0)
        cell_position.x = chunk.position.x
        cell_position.y = chunk.position.y
        cell_position.x += (x * 1.0 + y * 0.5 - int(y / 2)) * (HexMetrics().inner_radius * 2.0)
        cell_position.y += y * (HexMetrics().outer_radius * 1.5)
        
        cell = HexCell(cell_position.x, cell_position.y)
        cell.chunk = chunk
        self.cells.append(cell)
        chunk.cells.append(cell)

