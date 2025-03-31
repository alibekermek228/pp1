import pygame, json
from game_objects import Player, Food, Wall
import os

# Загрузка цветов
file_path = os.path.join(os.path.dirname(__file__), 'color.json')
with open(file_path) as f:
    color = json.load(f)

pygame.init()

# Настройки окна
SIZE = 400
win = pygame.display.set_mode((SIZE, SIZE))
pygame.display.set_caption('Snake')

# Функция для отрисовки фона
def fill_background(surface, level, balance, n_to_next_lvl):
    surface.fill(color['bg_color'])
    font = pygame.font.SysFont('comicsansms', 35)
    surface.blit(font.render(f'LVL: {level}', True, color['text']), (10, 10))
    surface.blit(font.render(f'Need: {balance}/{n_to_next_lvl}', True, color['text']), (200, 10))
    for i in range(0, SIZE, 20):
        pygame.draw.line(surface, color['black'], (i, 0), (i, SIZE), 2)
        pygame.draw.line(surface, color['black'], (0, i), (SIZE, i), 2)

# Инициализация игры
LEVEL, BALANCE, N_to_next_lvl, speed = 1, 0, 5, 5
wall, player, food = Wall(LEVEL), Player([]), Food([])
clock, run, losed = pygame.time.Clock(), True, None

while run:
    k_down_events = [event for event in pygame.event.get() if event.type == pygame.KEYDOWN]
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN and event.key in (pygame.K_RETURN, pygame.K_KP_ENTER) and losed:
            LEVEL, BALANCE, speed, losed = 1, 0, 5, None
            wall, player, food = Wall(LEVEL), Player([]), Food([])
    
    if losed is None:
        player.process_input(k_down_events)
        fill_background(win, LEVEL, BALANCE, N_to_next_lvl)
        losed = wall.can_go(player.points[0], player.dx, player.dy) or player.move(SIZE, SIZE)
        if food.can_eat(player.points[0]):
            player.add(player.points[0])
            BALANCE += 1
            if BALANCE == N_to_next_lvl:
                LEVEL, BALANCE = LEVEL + 1, 0
                wall, player = Wall(LEVEL), Player([])
                speed += 2 if LEVEL <= 3 else 8
                N_to_next_lvl = 999 if LEVEL > 3 else N_to_next_lvl
            food.change_pos(player.points + wall.points)
        player.draw(win), food.draw(win), wall.draw(win)
    else:
        pygame.draw.line(win, color['red'], (player.points[0].x, player.points[0].y), (player.points[0].x + 20, player.points[0].y + 20), 2)
        win.blit(pygame.font.SysFont('comicsansms', 80).render('You Lose', True, color['red']), (30, 120))
    
    pygame.display.update()
    clock.tick(speed)

pygame.quit()