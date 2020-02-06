import sys

import pygame

pygame.init()

size = width, height = 800, 600
speed = [0, 0]
black = 0, 0, 0

screen = pygame.display.set_mode(size)

player = pygame.image.load("player.png")
player_rect = player.get_rect()

speed[1] = 1

player_rect.top = 0
player_rect.left = 0

while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()

    player_rect = player_rect.move(speed)

    if (player_rect.bottom >= height) or (player_rect.top <= 0):
        speed[1] = -speed[1]

    speed[1] = speed[1] + 0.01

    screen.fill(black)
    screen.blit(player, player_rect)
    pygame.display.flip()
