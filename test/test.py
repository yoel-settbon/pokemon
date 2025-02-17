import pygame

pygame.init()
pygame.mixer.init()

pygame.mixer.music.load('assets/audio/battle-theme.wav')
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(1.0)

while True:
    pass
