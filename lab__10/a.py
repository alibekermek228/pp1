import psycopg2
import pygame
import sys
import random
import time

# --- PostgreSQL Setup ---
conn = psycopg2.connect(
    host="localhost",
    database="snake_game",
    user="postgres",
    password="postgres",
    port="5432"
)
cur = conn.cursor()

# Создание таблиц
cur.execute('''
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL
);
''')

cur.execute('''
CREATE TABLE IF NOT EXISTS user_scores (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    score INTEGER DEFAULT 0,
    level INTEGER DEFAULT 1,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
''')
conn.commit()

# --- Pygame Setup ---
pygame.init()
SW, SH = 800, 800
BLOCK_SIZE = 50
sc = pygame.display.set_mode((SW, SH))
pygame.display.set_caption("SNAKE")
clock = pygame.time.Clock()
font = pygame.font.Font(None, 50)

# --- Game State Variables ---
game_over = False
score = 0
level = 1
speed = 5
paused = False

# --- Input Username ---
username = input("Enter your username: ")
cur.execute("SELECT id FROM users WHERE username = %s", (username,))
user = cur.fetchone()
if not user:
    cur.execute("INSERT INTO users (username) VALUES (%s) RETURNING id", (username,))
    user_id = cur.fetchone()[0]
    conn.commit()
else:
    user_id = user[0]

# --- Snake Class ---
class Snake:
    def __init__(self):
        self.x, self.y = BLOCK_SIZE, BLOCK_SIZE
        self.xdir, self.ydir = 1, 0
        self.head = pygame.Rect(self.x, self.y, BLOCK_SIZE, BLOCK_SIZE)
        self.body = [pygame.Rect(self.x - BLOCK_SIZE, self.y, BLOCK_SIZE, BLOCK_SIZE)]
        self.dead = False

    def update(self):
        global game_over
        for square in self.body:
            if self.head.x == square.x and self.head.y == square.y:
                self.dead = True
        if self.head.x not in range(0, SW) or self.head.y not in range(0, SH):
            self.dead = True
        if self.dead:
            game_over = True
            return

        self.body.append(self.head)
        for i in range(len(self.body) - 1):
            self.body[i].x, self.body[i].y = self.body[i + 1].x, self.body[i + 1].y
        self.head.x += self.xdir * BLOCK_SIZE
        self.head.y += self.ydir * BLOCK_SIZE
        self.body.remove(self.head)

# --- Apple Class ---
class Applee:
    def __init__(self):
        self.respawn()

    def respawn(self):
        while True:
            self.x = random.randint(0, SW // BLOCK_SIZE - 1) * BLOCK_SIZE
            self.y = random.randint(0, SH // BLOCK_SIZE - 1) * BLOCK_SIZE
            self.ves = random.choice([1, 3, 5])
            self.color = {"yellow": (255, 255, 0), "red": (255, 0, 0), "white": (255, 255, 255)}[
                ["yellow", "red", "white"][random.randint(0, 2)]]
            self.rect = pygame.Rect(self.x, self.y, BLOCK_SIZE, BLOCK_SIZE)
            self.spawn_time = time.time()
            if not any(part.x == self.x and part.y == self.y for part in snake.body) and not (
                    snake.head.x == self.x and snake.head.y == self.y):
                break

    def update(self):
        pygame.draw.rect(sc, self.color, self.rect)
        if time.time() - self.spawn_time > 10:
            self.respawn()

# --- Helpers ---
def drawGrid():
    for x in range(0, SW, BLOCK_SIZE):
        for y in range(0, SH, BLOCK_SIZE):
            rect = pygame.Rect(x, y, BLOCK_SIZE, BLOCK_SIZE)
            pygame.draw.rect(sc, (255, 255, 255), rect, 1)

def reset_game():
    global snake, apple, game_over, score, level, speed
    snake = Snake()
    apple = Applee()
    game_over = False
    score = 0
    level = 1
    speed = 5

# --- Main Loop ---
reset_game()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            cur.close()
            conn.close()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if not game_over:
                if event.key == pygame.K_DOWN:
                    snake.xdir, snake.ydir = 0, 1
                elif event.key == pygame.K_UP:
                    snake.xdir, snake.ydir = 0, -1
                elif event.key == pygame.K_RIGHT:
                    snake.xdir, snake.ydir = 1, 0
                elif event.key == pygame.K_LEFT:
                    snake.xdir, snake.ydir = -1, 0
                elif event.key == pygame.K_p:
                    paused = not paused
                    if paused:
                        cur.execute(
                            "INSERT INTO user_scores (user_id, score, level) VALUES (%s, %s, %s)",
                            (user_id, score, level))
                        conn.commit()
            if event.key == pygame.K_r and game_over:
                reset_game()

    if not game_over and not paused:
        snake.update()

    sc.fill((0, 0, 0))
    drawGrid()

    if not paused:
        apple.update()

    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    sc.blit(score_text, (10, 10))
    level_text = font.render(f"Level: {level}", True, (0, 0, 255))
    sc.blit(level_text, (10, 50))

    pygame.draw.rect(sc, (0, 255, 0), snake.head)
    for square in snake.body:
        pygame.draw.rect(sc, (0, 255, 0), square)

    if snake.head.x == apple.x and snake.head.y == apple.y:
        score += apple.ves
        snake.body.append(pygame.Rect(square.x, square.y, BLOCK_SIZE, BLOCK_SIZE))
        apple.respawn()
        if score % 4 == 0:
            level += 1
            speed += 1

    if game_over:
        game_over_text = font.render("GAME OVER - Press R to Restart", True, (255, 0, 0))
        sc.blit(game_over_text, (SW // 4, SH // 2))

    pygame.display.update()
    clock.tick(speed)
   


