import pygame
import sys
import random
import time

pygame.init()

SW = 800
SH = 800
BLOCK_SIZE = 50 

sc = pygame.display.set_mode((SW, SH))
pygame.display.set_caption("SNAKE")
clock = pygame.time.Clock()
font = pygame.font.Font(None, 50)

game_over = False
level = 1  
speed = 5  # Starter velocity
score = 0  # Starter score

class Snake:
    def __init__(self):
        self.x, self.y = BLOCK_SIZE, BLOCK_SIZE # starter position
        self.xdir = 1 # action right
        self.ydir = 0
        self.head = pygame.Rect(self.x, self.y, BLOCK_SIZE, BLOCK_SIZE) # its snnke head
        self.body = [pygame.Rect(self.x - BLOCK_SIZE, self.y, BLOCK_SIZE, BLOCK_SIZE)] # its snake body
        self.dead = False

    def update(self):
        global game_over
        for square in self.body:
            if self.head.x == square.x and self.head.y == square.y:
                self.dead = True # if snake врезалась yourself

        if self.head.x not in range(0, SW) or self.head.y not in range(0, SH):
            self.dead = True # if snake out of limit in our window

        if self.dead:
            game_over = True
            return # end to play

        self.body.append(self.head) # add head in body
        for i in range(len(self.body) - 1):
            self.body[i].x, self.body[i].y = self.body[i+1].x, self.body[i+1].y
        self.head.x += self.xdir * BLOCK_SIZE
        self.head.y += self.ydir * BLOCK_SIZE
        self.body.remove(self.head) # when snake start to go

class Applee:

    def __init__(self):
        self.respawn() # generate apple


    def respawn(self):
        while True:
            self.x = random.randint(0, SW // BLOCK_SIZE - 1) * BLOCK_SIZE
            self.y = random.randint(0, SH // BLOCK_SIZE - 1) * BLOCK_SIZE
            self.ves = random.choice([1,3,5])
            self.color = {1: "yellow", 3: "red", 5:"white"}[self.ves] # weight and color on the apple
            self.rect = pygame.Rect(self.x, self.y, BLOCK_SIZE, BLOCK_SIZE)
            self.spawn_time = time.time()

            if not any(part.x == self.x and part.y == self.y for part in snake.body) and not (snake.head.x == self.x and snake.head.y == self.y):
                break # apple don't appear in snake

    def update(self):
        pygame.draw.rect(sc, self.color, self.rect)
        if time.time() - self.spawn_time > 10: import pygame
import datetime

# Initialize Pygame
pygame.init()

# Screen settings
W, H = 800, 800
screen = pygame.display.set_mode((W, H))
pygame.display.set_caption("Clock")
clock = pygame.time.Clock()

# Load clock face and hands images
clock_face = pygame.transform.scale(pygame.image.load("clock.png"), (600, 600))
hands = {
    "minute": pygame.transform.scale(pygame.image.load("min_hand.png"), (600, 900)), 
    "second": pygame.transform.scale(pygame.image.load("sec_hand.png"), (250, 500)),
}

# Constants
CENTER = (W // 2, H // 2)
FPS = 50

# Main loop
running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Get current time
    now = datetime.datetime.now()
    angles = {
        "minute": -now.minute * 6,
        "second": -now.second * 6,
    }

    # Update screen
    screen.fill((255, 255, 255))
    screen.blit(clock_face, (100, 100))

    # Rotate and draw hands
    for hand, img in hands.items():
        rotated_hand = pygame.transform.rotate(img, angles[hand])
        rect = rotated_hand.get_rect(center=CENTER)
        screen.blit(rotated_hand, rect.topleft)

    # Draw center circle
    pygame.draw.circle(screen, (0, 0, 0), CENTER, 10)

    # Update display
    pygame.display.flip()

    # Control the frame rate
    clock.tick(FPS)

# Quit Pygame
pygame.quit()


def drawGrid():
    for x in range(0, SW, BLOCK_SIZE):
        for y in range(0, SH, BLOCK_SIZE):
            rect = pygame.Rect(x, y, BLOCK_SIZE, BLOCK_SIZE)
            pygame.draw.rect(sc, (255,255,255), rect, 1)

def reset_game(): 
    global snake, apple, game_over, level, speed,score 
    snake = Snake()
    apple = Applee()
    game_over = False
    level = 1  
    speed = 5
    score = 0

drawGrid() 
snake = Snake()
apple = Applee()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if not game_over:
                if event.key == pygame.K_DOWN:
                    snake.xdir = 0
                    snake.ydir = 1
                elif event.key == pygame.K_UP:
                    snake.xdir = 0
                    snake.ydir = -1
                elif event.key == pygame.K_RIGHT:
                    snake.xdir = 1
                    snake.ydir = 0
                elif event.key == pygame.K_LEFT:
                    snake.ydir = 0
                    snake.xdir = -1
            if event.key == pygame.K_r and game_over:
                reset_game() 

    if not game_over:
        snake.update() 

    sc.fill((0,0,0))
    drawGrid()

    apple.update()

    
    score_rect = font.render(f"Score:{score}", True, "white")
    sc.blit(score_rect, (10, 10))

    
    level_rect = font.render(f"Level: {level}", True, "Blue")
    sc.blit(level_rect, (10, 50))

    
    pygame.draw.rect(sc, "green", snake.head)
    for square in snake.body:
        pygame.draw.rect(sc, "green", square)

    
    if snake.head.x == apple.x and snake.head.y == apple.y:
        score += apple.ves
        snake.body.append(pygame.Rect(square.x, square.y, BLOCK_SIZE, BLOCK_SIZE))
        apple.respawn()

        
        if score % 4 == 0:
            level += 1
            speed += 3/2

    if game_over: 
        game_over_text = font.render("GAME OVER - Press R to Restart", True, (255, 0, 0))
        sc.blit(game_over_text, (SW // 4, SH // 2))

    pygame.display.update()
    clock.tick(speed) 