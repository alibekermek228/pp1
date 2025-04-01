import pygame

pygame.init()

r = 25
x = 30
y = 30
w = 600
h = 600
WHITE = (255,255,255)
RED = (255,0,0)
speed = 20


a = pygame.display.set_mode((w,h))
pygame.display.set_caption('Circle')

Clock = pygame.time.Clock()
running = True
while running:
     a.fill(WHITE)
     pygame.draw.circle(a, (255,0,0),(x,y), r)
     Clock.tick(60)
     for event in pygame.event.get():
          if event.type == pygame.QUIT:
               running = False
     keys = pygame.key.get_pressed()

     if(keys[pygame.K_LEFT] and x>r):
          x-=speed
     if(keys[pygame.K_RIGHT] and x<w-r):
          x+=speed
     if(keys[pygame.K_UP] and y >r):
          y-=speed
     if(keys[pygame.K_DOWN] and y<h-r):
          y+=speed
     

     
     pygame.display.flip()

pygame.quit()
