import pygame
pygame.init()
pygame.mixer.init()

playlist = [
    ("track1.mp3"),
    ("track2.mp3"),
    ("track3.mp3")
]

running = True
current_track = 0

def play_music():
    pygame.mixer.music.load(playlist[current_track])
    pygame.mixer.music.play()

a = pygame.display.set_mode((600,600))
pygame.display.set_caption('Music player')
font = pygame.font.Font(None, 25)

play_music()

while running:
    a.fill((0,255,0))
    b = font.render("SPACE = PAUSE, S - STOP, N - NEXT, P - PREVIOUS", True , (255,255,255))
    a.blit(b, (20,130))
    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if(event.key == pygame.K_SPACE):
                if pygame.mixer.music.get_busy():
                    pygame.mixer.music.pause()
                else:
                    pygame.mixer.music.unpause()
            elif event.key == pygame.K_s:
                pygame.mixer.music.stop()
            elif event.key == pygame.K_n:
                
                current_track = (current_track + 1) % len(playlist)

                play_music()
            elif event.key == pygame.K_p:
                current_track = (current_track - 1) % len(playlist)
                play_music()
pygame.quit()