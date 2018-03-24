import pygame, random, pickle
from HexMetrics import *
from HexCoordinates import *
from HexMesh import *
pygame.init()
class HexChunk(object):
    font = pygame.font.Font(None, 30)
    
    SURFACE_PADDING = Vector2(100,100)
    
    def __init__(self, position):
        self.position = position
        self.coordinates = HexCoordinates().from_position(self.position)
        self.cells = []
        self.mesh = HexMesh()
        self.enabled = True
        self.surface = pygame.Surface(
            (HexMetrics().chunk_width * 1.5, HexMetrics().chunk_height * 1.5),
            pygame.SRCALPHA)
        self.surface.fill((0,0,0,0))

    def __eq__(self, other):
        return self.coordinates == other.coordinates

    def update(self):
        self.triangulate()
        self.triangles_to_surface()
        self.render_coordinates()
        self.surface = pygame.Surface.convert_alpha(self.surface)
        self.enabled = False

        
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
        
    def triangles_to_surface(self):
        for i in range(self.mesh.triangles):
            self.render_triangle(
                self.mesh.vertices[i * 3] - self.position + self.SURFACE_PADDING,
                self.mesh.vertices[(i * 3) + 1] - self.position + self.SURFACE_PADDING,
                self.mesh.vertices[(i * 3) + 2] - self.position + self.SURFACE_PADDING,
                self.mesh.colors[i]
            )
    
    def render_triangle(self, v1, v2, v3, color = (20, 150, 20)):
        # pygame.draw.polygon(self.surface, (random.randint(20,100), 150, random.randint(20,100)), (v1, v2, v3))
        pygame.draw.polygon(self.surface, color, (v1, v2, v3))

    def render_coordinates(self):
        for cell in self.cells:
            coordinate_surf = self.font.render(str(cell.coordinates), True, (0,0,0))
            self.surface.blit(coordinate_surf, HexMetrics().perturb(cell.position) - self.position + self.SURFACE_PADDING + Vector2(-25, -25))

    def serialize(self):
        with open(str(self.coordinates), 'wb') as handle:
            for cell in self.cells:
                pickle.dump(cell.colors, handle, protocol=pickle.HIGHEST_PROTOCOL)
    def deserialize(self):
        with open(str(self.coordinates), 'wb') as handle:
            for cell in self.cells:
                pickle.load(handle)