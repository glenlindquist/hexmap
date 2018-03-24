from pygame.math import *
from HexCell import *
from HexMetrics import *
from HexChunk import *
from pathlib import Path

class HexGrid(object):
    def __init__(self):
        self.chunks = []
        self.cell_count_x = 0
        self.cell_count_y = 0
        self.chunk_dict = {}

    def update(self):
        for chunk in self.chunk_dict:
            if self.chunk_dict[chunk].enabled:
                self.chunk_dict[chunk].update()

    def load_chunks(self, player):
        for offset in HexMetrics().chunk_offsets:
            chunk_position = player.chunk.to_position() + Vector2(offset[0], offset[1])
            chunk_file = Path(HexChunk.CHUNK_FOLDER + str(HexCoordinates().from_position(chunk_position)))
            if str(HexCoordinates().from_position(chunk_position)) in self.chunk_dict:
                # keep using the chunk from the dict of active chunks
                pass
            elif chunk_file.is_file():
                # load chunk from file
                chunk = HexChunk(chunk_position)
                chunk.deserialize()
                self.chunks.append(chunk)
                self.chunk_dict[str(chunk.coordinates)] = chunk
            else:
                # create new chunk
                chunk = HexChunk(chunk_position)
                chunk.create_cells()
                self.chunks.append(chunk)
                self.chunk_dict[str(chunk.coordinates)] = chunk


    def unload_chunks(self, player):
        chunks_to_remove = list(chunk for chunk in self.chunk_dict if
                                abs(self.chunk_dict[chunk].position.x - player.chunk.to_position().x) > HexMetrics().chunk_width or
                                abs(self.chunk_dict[chunk].position.y - player.chunk.to_position().y) > HexMetrics().chunk_height
                                )
        for chunk in chunks_to_remove:
            chunk_file = Path(HexChunk.CHUNK_FOLDER + chunk)
            if not chunk_file.is_file() or self.chunk_dict[chunk].changed:
                self.chunk_dict[chunk].serialize()
                self.chunk_dict[chunk].changed = False
            del self.chunk_dict[chunk]

    def get_cell_at_pos(self, position):
        chunk_coords = HexCoordinates().chunk_coordinates_containing(position)
        for cell in self.chunk_dict[str(chunk_coords)].cells:
            if cell.coordinates == HexCoordinates().from_position(position):
                return cell


