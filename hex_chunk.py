import pygame, random, pickle
from hex_metrics import *
from hex_coordinates import *
from hex_mesh import *
from hex_cell import *
pygame.init()
class HexChunk(object):
    # need a better way to get coordinates written so we don't need to init pygame twice
    font = pygame.font.Font(None, 30)

    CHUNK_FOLDER = "chunk_data/"
    
    SURFACE_PADDING = Vector2(100,100)
    
    def __init__(self, position):
        self.position = position
        self.coordinates = HexCoordinates().from_position(self.position)
        self.cells = []
        self.mesh = HexMesh()
        self.enabled = True
        self.surface = pygame.Surface(
            (HexMetrics.chunk_width * 1.5, HexMetrics.chunk_height * 1.5),
            pygame.SRCALPHA)
        self.surface.fill((0, 0, 0, 0))
        self.changed = False

    def __eq__(self, other):
        return self.coordinates == other.coordinates

    def clear(self):
        #del self.cells[:]
        del self.cells
        self.cells = []
        self.mesh.clear()
        self.enabled = True
        self.surface.fill((0, 0, 0, 0))
        self.changed = False

    def update(self):
        self.triangulate()
        self.triangles_to_surface()
        self.render_coordinates()
        self.surface = pygame.Surface.convert_alpha(self.surface)
        self.enabled = False

    def create_cells(self):
        for y in range(HexMetrics.chunk_size_y):
            for x in range(HexMetrics.chunk_size_x):
                self.create_cell(x, y)

    def create_cell(self, x, y):
        cell_position = Vector2(0, 0)
        cell_position.x = self.position.x
        cell_position.y = self.position.y
        cell_position.x += (x * 1.0 + y * 0.5 - int(y / 2)) * (HexMetrics.inner_radius * 2.0)
        cell_position.y += y * (HexMetrics.outer_radius * 1.5)

        cell = HexCell(cell_position.x, cell_position.y)
        cell.chunk = self
        self.cells.append(cell)

    def get_edge_cells(self):
        i = 0
        edge_cells = []
        for y in range(HexMetrics.chunk_size_y):
            for x in range(HexMetrics.chunk_size_x):
                if x == 0 or x == HexMetrics.chunk_size_x - 1 or y == 0 or y == HexMetrics.chunk_size_y-1:
                    edge_cells.append(self.cells[i])
                i += 1
        return edge_cells

    def triangulate_edge_cells(self, edge_cells):
        for cell in edge_cells:
            cell.change_terrain(3)
            self.triangulate_cell(cell)

    def triangulate(self):
        for cell in self.cells:
            self.triangulate_cell(cell)

    def triangulate_cell (self, cell):
        for direction in range(6):
            self.triangulate_wedge(direction, cell)
    
    def triangulate_wedge(self, direction, cell):
        center = cell.position
        ev1 = center + HexMetrics().get_first_corner(direction)
        ev2 = center + HexMetrics().get_second_corner(direction)
        self.mesh.add_triangle(center, ev1, ev2, cell.colors[direction])
        
    # method used for redundant vertices --------------------- #
    def triangles_to_surface(self):
        for i in range(self.mesh.triangles):
            self.render_triangle(
                self.mesh.vertices[i * 3] - self.position + self.SURFACE_PADDING,
                self.mesh.vertices[(i * 3) + 1] - self.position + self.SURFACE_PADDING,
                self.mesh.vertices[(i * 3) + 2] - self.position + self.SURFACE_PADDING,
                self.mesh.colors[i]
            )

    # method used if vertices shared ------------------------- #
    # def triangles_to_surface(self):
    #    indices = self.mesh.indices
    #    for i in range(self.mesh.triangles):
    #        self.render_triangle(
    #            self.mesh.vertices[indices[i * 3]] - self.position + self.SURFACE_PADDING,
    #            self.mesh.vertices[indices[(i * 3) + 1]] - self.position + self.SURFACE_PADDING,
    #            self.mesh.vertices[indices[(i * 3) + 2]] - self.position + self.SURFACE_PADDING,
    #            self.mesh.colors[i]
    #        )

    def render_triangle(self, v1, v2, v3, color = (20, 150, 20)):
        pygame.draw.polygon(self.surface, color, (v1, v2, v3))

    def render_coordinates(self):
        for cell in self.cells:
            coordinate_surf = self.font.render(str(cell.coordinates), True, (255, 0, 0))
            self.surface.blit(coordinate_surf, HexMetrics().perturb(cell.position) - self.position + self.SURFACE_PADDING + Vector2(-25, -25))

    def serialize(self):
        chunk_properties = []
        for i in range(len(self.cells)):
            chunk_properties.append(self.cells[i].colors)
            chunk_properties.append(self.cells[i].terrain)
        with open(self.CHUNK_FOLDER + str(self.coordinates), 'wb') as handle:
            pickle.dump(chunk_properties, handle, protocol=pickle.HIGHEST_PROTOCOL)

    def deserialize(self):
        with open(self.CHUNK_FOLDER + str(self.coordinates), 'rb') as handle:
            chunk_properties = pickle.load(handle)
        i = 0
        for y in range(HexMetrics.chunk_size_y):
            for x in range(HexMetrics.chunk_size_x):
                cell_position = Vector2(0, 0)
                cell_position.x = self.position.x
                cell_position.y = self.position.y
                cell_position.x += (x * 1.0 + y * 0.5 - int(y / 2)) * (HexMetrics.inner_radius * 2.0)
                cell_position.y += y * (HexMetrics.outer_radius * 1.5)
                cell = HexCell(cell_position.x, cell_position.y)
                cell.colors = chunk_properties[i]
                i += 1
                cell.terrain = int(chunk_properties[i])
                i += 1
                cell.chunk = self
                self.cells.append(cell)

