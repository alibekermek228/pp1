import pygame
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

