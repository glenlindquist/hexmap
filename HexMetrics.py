import pygame
import os
from pygame.math import *
from enum import IntEnum

class HexMetrics(object):
    """Defining a Hexagon"""
    # Scale
    SCALE = 8
    
    # Basic hex constants
    outer_to_inner = 0.866025404
    inner_to_outer = 1.0 / outer_to_inner
    outer_radius = 10.0 * SCALE
    inner_radius = outer_radius * outer_to_inner
    
    hex_width = inner_radius * 2.0
    hex_height = outer_radius * 2.0
    
    # Blending gap between hexes
    solid_factor = 0.8
    blend_factor = 1.0 - solid_factor
    
    # Chunk constants
    # Ideally these should be kept to even numbers
    chunk_size_x = 4
    chunk_size_y = 4
    
    chunk_width = chunk_size_x * hex_width
    # height is different because rows are staggered
    chunk_height = chunk_size_y * outer_radius * 1.5
    
    # Perturbation constants
    noise_source = os.path.join('Textures', 'Noise.png')
    noise_dimension_x = 512
    noise_dimension_y = 512
    noise_surface = pygame.image.load(noise_source)
    noise_scale = 1.0
    cell_perturb_strength =  0.025 * SCALE
    
    # pointy-topped hex, starting at top, going clockwise
    corners = [
        Vector2(0.0, outer_radius),
        Vector2(inner_radius, 0.5 * outer_radius),
        Vector2(inner_radius, -0.5 * outer_radius),
        Vector2(0.0, -outer_radius),
        Vector2(-inner_radius, -0.5 * outer_radius),
        Vector2(-inner_radius, 0.5 * outer_radius),
        Vector2(0.0,outer_radius)
    ]

    chunk_offsets = [
        [0.0, 0.0],
        [chunk_width, 0.0],
        [-chunk_width, 0.0],
        [chunk_width, chunk_height],
        [-chunk_width, -chunk_height],
        [-chunk_width, chunk_height],
        [chunk_width, -chunk_height],
        [0.0, chunk_height],
        [0.0, -chunk_height]
    ]
    
    def get_first_corner(self, direction):
        return self.corners[int(direction)]
        
    def get_second_corner(self, direction):
        return self.corners[int(direction)+1]
        
    def get_first_solid_corner(self, direction):
        return self.corners[int(direction)] * self.solid_factor
        
    def get_second_solid_corner(self, direction):
        return self.corners[int(direction)] * self.solid_factor
        
    def sample_noise(self, pos):
        #print("pre_x:", pos.x, "pre_y:", pos.y)
        sample_location_x = abs(round(pos.x * self.noise_scale))
        while sample_location_x >= self.noise_dimension_x:
            sample_location_x -= self.noise_dimension_x
        while sample_location_x < 0:
            sample_location_x += self.noise_dimension_x

            
        sample_location_y = abs(round(pos.y * self.noise_scale))
        while sample_location_y >= self.noise_dimension_y:
            sample_location_y -= self.noise_dimension_y
        while sample_location_y < 0:
            sample_location_y += self.noise_dimension_y

        return self.noise_surface.get_at((sample_location_x, sample_location_y))
    
    def perturb(self, pos):
        sample = self.sample_noise(pos)
        new_pos = Vector2(0,0)
        new_pos.x = pos.x
        new_pos.y = pos.y
        new_pos.x += (sample.b) * self.cell_perturb_strength
        new_pos.y += (sample.g) * self.cell_perturb_strength
        return new_pos
        
class HexDirection(IntEnum):
    NE = 1
    E = 2
    SE = 3
    SW = 4
    W = 5
    NW = 6
    
    def opposite(self):
        if self < 3:
            return self + 3
        else:
            return self - 3
    
    def previous(self):
        if self == HexDirection.NE:
            return HexDirection.NW
        else:
            return self - 1
            
    def next(self):
        if self == HexDirection.NW:
            return HexDirection.NE
        else:
            return self + 1
    
    def previous2(self):
        self -= 2
        if self >= HexDirection.NE:
            return self
        else:
            return self + 6
        
    def next2(self):
        self += 2
        if self <= HexDirection.NW:
            return self
        else:
            return self - 6   
