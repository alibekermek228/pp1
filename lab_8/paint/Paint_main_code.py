import pygame
from pygame.locals import *

pygame.init()

WIDTH, HEIGHT = 800, 600
WHITE, BLACK = (255, 255, 255), (0, 0, 0)
colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0)]

screen = pygame.display.set_mode((WIDTH, HEIGHT))
canvas = pygame.Surface((WIDTH, HEIGHT))
canvas.fill(WHITE)

clock = pygame.time.Clock()
brush_size, mode, color = 5, 'draw', BLACK

def draw_shape(pos, shape='circle'):
    if shape == 'circle':
        pygame.draw.circle(canvas, color, pos, brush_size)
    elif shape == 'rect':
        pygame.draw.rect(canvas, color, (*pos, brush_size * 2, brush_size * 2))

def handle_events():
    global mode, color, brush_size
    for event in pygame.event.get():
        if event.type == QUIT:
            return False
        elif event.type == KEYDOWN:
            if event.key == K_c:
                canvas.fill(WHITE)
            elif event.key == K_UP:
                brush_size = min(50, brush_size + 2)
            elif event.key == K_DOWN:
                brush_size = max(2, brush_size - 2)
            elif event.key == K_e:
                mode, color = 'erase', WHITE
            elif event.key == K_d:
                mode, color = 'draw', BLACK
            elif event.key in [K_1, K_2, K_3, K_4]:
                color = colors[event.key - K_1]
    return True

going = True
while going:
    going = handle_events()
    if pygame.mouse.get_pressed()[0]:
        draw_shape(pygame.mouse.get_pos(), 'circle')
    screen.blit(canvas, (0, 0))
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
