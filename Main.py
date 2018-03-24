#!/usr/bin/python3.6

# ------------------------------------------------------------ #
# Glen Lindquist                                               # 
# glenlindquist@gmail.com                                      #
# ------------------------------------------------------------ #

# Setup Python ----------------------------------------------- #
import sys, pygame, random
import pygame.gfxdraw
from pygame.math import *
from pygame.locals import *

from hex_metrics import *
from hex_chunk import *
from hex_grid import *
from hex_mesh import *
from player import *

# Setup pygame/window ---------------------------------------- #
pygame.init()
FPS = 60
fpsClock = pygame.time.Clock()

WINDOWWIDTH = 800
WINDOWHEIGHT = 600
CENTER_X = WINDOWWIDTH / 2
CENTER_Y = WINDOWHEIGHT / 2
CENTER = Vector2(CENTER_X, CENTER_Y)
DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()
pygame.mixer.set_num_channels(32)
pygame.display.set_caption("Hex Map")
random.seed()

# Colors ----------------------------------------------------- #
BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)

def random_green():
    return (random.randint(20,100), 150, random.randint(20,100))


# Images ----------------------------------------------------- #

# Text ------------------------------------------------------- #
font = pygame.font.Font(None, 30)

# Functions -------------------------------------------------- #
#def render_mesh(mesh, offset = Vector2(0,0)):
#    for i in range(mesh.triangles):
#        render_triangle(
#            mesh.vertices[mesh.indices[i * 3]] + offset, 
#            mesh.vertices[mesh.indices[(i * 3) + 1]] + offset, 
#            mesh.vertices[mesh.indices[(i * 3) + 2]] + offset
#        )

#Old method, without shared verts
def render_mesh(surface, mesh, offset = Vector2(0,0)):
    for i in range(mesh.triangles):
        render_triangle(
            surface,
            mesh.vertices[i * 3] + offset, 
            mesh.vertices[(i * 3) + 1] + offset, 
            mesh.vertices[(i * 3) + 2] + offset
        )

def render_triangle(surface, v1, v2, v3):
     pygame.draw.polygon(surface, random_green(), ((0,0), (0,50), (50,0)))
   
     #pygame.draw.polygon(surface, random_green(), (v1, v2, v3))

#Slower draw methods, but more options
#    pygame.gfxdraw.filled_trigon(
#        DISPLAYSURF,
#        round(v1.x), round(v1.y),
#        round(v2.x), round(v2.y),
#        round(v3.x), round(v3.y),
#        random_green()
#    )
#    pygame.gfxdraw.aatrigon(
#         DISPLAYSURF,
#        round(v1.x), round(v1.y),
#        round(v2.x), round(v2.y),
#        round(v3.x), round(v3.y),
#        BLACK    
#    )



# Controller ------------------------------------------------- #

# Audio ------------------------------------------------------ #

# Variables -------------------------------------------------- #


PLAYER_SPEED = 10  # pixels/frame
PLAYER_RADIUS = 10

player_model = pygame.Surface((21, 21), pygame.SRCALPHA)
player_model.fill((0,0,0,0))
pygame.gfxdraw.filled_circle(player_model, PLAYER_RADIUS, PLAYER_RADIUS, PLAYER_RADIUS, BLACK)


# Initialization --------------------------------------------- #


grid = HexGrid()
player = Player(Vector2(0, 0))
grid.load_chunks(player)
right = False
left = False
up = False
down = False
space = False

update_map = True
redraw_triangles = True
DISPLAYSURF.fill(GREEN)


# Game loop -------------------------------------------------- #
while True:
    # Background --------------------------------------------- #

    # Buttons ------------------------------------------------ #
    key_pressed = False
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == KEYDOWN:
            key_pressed = True
            if event.key == K_d:                
                right = True
            elif event.key == K_a:
                left = True
            elif event.key == K_w:
                up = True
                update_map = True
            elif event.key == K_s:
                down = True
            elif event.key == K_SPACE:
                space = True
        elif event.type == KEYUP:
            key_pressed = False
            if event.key == K_d:
                right = False
            elif event.key == K_a:
                left = False
            elif event.key == K_w:
                up = False
            elif event.key == K_s:
                down = False
            elif event.key == K_SPACE:
                space = False
    # Player Movement ---------------------------------------- #
    if right:
        player.position.x += PLAYER_SPEED
    if left:
        player.position.x -= PLAYER_SPEED
    if up:
        player.position.y -= PLAYER_SPEED
    if down:
        player.position.y += PLAYER_SPEED
    if space:
        player_cell = grid.get_cell_at_pos(player.position)
        player_cell.change_terrain(1)
    # Update map --------------------------------------------- #
    if True: #replace with update_display
        # DISPLAYSURF.fill(GREEN)
        grid.update()
        # if redraw_triangles:
        #    for chunk in grid.chunks:
        #        render_mesh(chunk.surface, chunk.mesh, (0,0))
        #    redraw_triangles = False
        for chunk in grid.chunks:
            DISPLAYSURF.blit(chunk.surface, chunk.position + CENTER - player.position - chunk.SURFACE_PADDING)

    old_player_chunk = player.chunk
    player.chunk = HexCoordinates().chunk_coords_containing_pos(player.position)
    if old_player_chunk != player.chunk:
        # print("chunk mismatch")
        grid.load_chunks(player)
        grid.unload_chunks(player)

    player.coordinates = HexCoordinates().from_position(player.position)

    # Update ------------------------------------------------- #
    fps_counter = font.render(str(int(fpsClock.get_fps())), True, WHITE)
    # player_chunk = font.render(str(player.chunk), True, WHITE)
    # player_cell_position = font.render(str(player.coordinates), True, WHITE)
    # player_position = font.render(str(player.position),True, WHITE)
    DISPLAYSURF.blit(fps_counter, (50,50))
    # DISPLAYSURF.blit(player_chunk, (50,100))
    DISPLAYSURF.blit(player_model, (CENTER.x - PLAYER_RADIUS, CENTER.y - PLAYER_RADIUS))
    # DISPLAYSURF.blit(player_cell_position, (50, 150))
    # DISPLAYSURF.blit(player_position, (50, 200))

    pygame.display.update()
    fpsClock.tick(FPS)