import pygame
from math import *
import random

# colors
red = (255, 0, 0)
yellow = (255, 255, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
white = (255, 255, 255)
black = (0, 0, 0)
colors = [red, green, blue, white, yellow]

# ===== SETTINGS ===== #
focal_length = 64
scroll_amount = 10
render_vertices = True
render_edges = True
angle_rotation = 1
angle_rotation_value = 0.025
default_color = red
vertex_color = white
random_colors = True

breathing = 0
change_breathing = 1

x_offset = 0
y_offset = 0
x_change = 0
y_change = 0

x_rotating = 0
y_rotating = 0
z_rotating = 0

fps = 144
fpsclock = pygame.time.Clock()

class Vertex():
    def __init__(self, x: int, y: int, z: int):
        self.x = x
        self.y = y
        self.z = z

        self.x_projected = (focal_length * self.x) // (focal_length + self.z + 128) + 100
        self.y_projected = (focal_length * self.y) // (focal_length + self.z + 128) + 100
    
    def move(self):
        self.x_projected = (focal_length * self.x) // (focal_length + self.z + 128) + 100
        self.y_projected = (focal_length * self.y) // (focal_length + self.z + 128) + 100

    def draw(self):
        pygame.draw.circle(DISPLAY, vertex_color, (self.x_projected * 5 + x_offset, self.y_projected * 5 + y_offset), 5)

class Edge():
    def __init__(self, vertex_1: Vertex, vertex_2: Vertex, color: tuple) -> None:
        self.vertex_1 = vertex_1
        self.vertex_2 = vertex_2
        self.color = color
    
    def draw(self):
        pygame.draw.line(DISPLAY, self.color if random_colors else default_color, (self.vertex_1.x_projected * 5 + x_offset, self.vertex_1.y_projected * 5 + y_offset), (self.vertex_2.x_projected * 5 + x_offset, self.vertex_2.y_projected * 5 + y_offset), 2)

# Edit Vertexes and Edges, currently hardcoded, but you can draw any shape

a_vertex = Vertex(64, 64, 64)
b_vertex = Vertex(64, -64, 64)
c_vertex = Vertex(-64, -64, 64)
d_vertex = Vertex(-64, 64, 64)
e_vertex = Vertex(64, 64, -64)
f_vertex = Vertex(64, -64, -64)
g_vertex = Vertex(-64, -64, -64)
h_vertex = Vertex(-64, 64, -64)

a_b_edge = Edge(a_vertex, b_vertex, random.choice(colors))
b_c_edge = Edge(b_vertex, c_vertex, random.choice(colors))
c_d_edge = Edge(c_vertex, d_vertex, random.choice(colors))
d_a_edge = Edge(d_vertex, a_vertex, random.choice(colors))
e_f_edge = Edge(e_vertex, f_vertex, random.choice(colors))
f_g_edge = Edge(f_vertex, g_vertex, random.choice(colors))
g_h_edge = Edge(g_vertex, h_vertex, random.choice(colors))
h_e_edge = Edge(h_vertex, e_vertex, random.choice(colors))
a_e_edge = Edge(a_vertex, e_vertex, random.choice(colors))
b_f_edge = Edge(b_vertex, f_vertex, random.choice(colors))
c_g_edge = Edge(c_vertex, g_vertex, random.choice(colors))
d_h_edge = Edge(d_vertex, h_vertex, random.choice(colors))

vertices = [a_vertex, b_vertex, c_vertex, d_vertex, e_vertex, f_vertex, g_vertex, h_vertex]
edges = [a_b_edge, b_c_edge, c_d_edge, d_a_edge, e_f_edge, f_g_edge, g_h_edge, h_e_edge, a_e_edge, b_f_edge, c_g_edge, d_h_edge]


def draw():
    DISPLAY.fill(black)
    if render_edges:
        for edge in edges:
            edge.draw()
    
    if render_vertices:
        for vertex in vertices:
            vertex.draw()

def move_shape(x_offset: int, y_offset: int) -> tuple:
    for vertex in vertices:
        vertex.move()

    x_offset += x_change
    y_offset += y_change

    for vertex in vertices:
        if x_rotating > 0:
            vertex.y, vertex.z = rotate_x(vertex, angle_rotation_value)

        if y_rotating > 0:
            vertex.x, vertex.z = rotate_y(vertex, angle_rotation_value)
        
        if z_rotating > 0:
            vertex.y, vertex.x = rotate_z(vertex, angle_rotation_value)
        
        if x_rotating < 0:
            vertex.y, vertex.z = rotate_x(vertex, -angle_rotation_value)

        if y_rotating < 0:
            vertex.x, vertex.z = rotate_y(vertex, -angle_rotation_value)
        
        if z_rotating < 0:
            vertex.y, vertex.x = rotate_z(vertex, -angle_rotation_value)



    return (x_offset, y_offset)

def rotate_x(vertex: Vertex, angle: int) -> tuple:
    return (vertex.y * cos(angle) + vertex.z * sin(angle), vertex.z * cos(angle) - vertex.y * sin(angle))

def rotate_y(vertex: Vertex, angle: int) -> tuple:
    return (vertex.x * cos(angle) + vertex.z * sin(angle), vertex.z * cos(angle) - vertex.x * sin(angle))

def rotate_z(vertex: Vertex, angle: int) -> tuple:
    return (vertex.y * cos(angle) + vertex.x * sin(angle), vertex.x * cos(angle) - vertex.y * sin(angle))


pygame.init()
DISPLAY = pygame.display.set_mode((1000, 1000))
pygame.display.set_caption("3d Renderer")

while True:
    fpsclock.tick(fps)
    draw()
    x_offset, y_offset = move_shape(x_offset, y_offset)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                x_change = 1
            
            elif event.key == pygame.K_LEFT:
                x_change = -1

            elif event.key == pygame.K_UP:
                y_change = -1
            
            elif event.key == pygame.K_DOWN:
                y_change = 1
            
            elif event.key == pygame.K_d:
                y_rotating = -1
                
            elif event.key == pygame.K_a:
                y_rotating = 1
            
            elif event.key == pygame.K_w:
                x_rotating = 1
                
            elif event.key == pygame.K_s:
                x_rotating = -1
            
            elif event.key == pygame.K_q:
                z_rotating = -1
                
            elif event.key == pygame.K_e:
                z_rotating = 1
            
            elif event.key == pygame.K_z:
                random_colors = not random_colors
            
            elif event.key == pygame.K_x:
                render_vertices = not render_vertices
            
            elif event.key == pygame.K_c:
                render_edges = not render_edges
        
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT:
                x_change = 0

            elif event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                y_change = 0
            
            elif event.key == pygame.K_d or event.key == pygame.K_a:
                y_rotating = 0
            
            elif event.key == pygame.K_w or event.key == pygame.K_s:
                x_rotating = 0
            
            elif event.key == pygame.K_e or event.key == pygame.K_q:
                z_rotating = 0
        
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 4:
                if focal_length <= 800:
                    focal_length += scroll_amount
                
            elif event.button == 5:
                if focal_length >= 15:
                    focal_length -= scroll_amount
        
        elif event.type == pygame.MOUSEBUTTONUP:
            change_focal_length = 0
    
    pygame.display.update()