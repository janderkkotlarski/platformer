import sys

import pygame

pygame.init()

size = width, height = 1024, 768
speed = [0, 0]
black = 0, 0, 0

screen = pygame.display.set_mode(size)

player = pygame.image.load("player.png")
player_rect = player.get_rect()


while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()

    player_rect = player_rect.move(speed)

    if player_rect.bottom > height:
        speed[1] = -speed[1]
        player_rect.bottom = height + 1

    speed[1] = speed[1] + 1

    screen.fill(black)
    screen.blit(player, player_rect)
    pygame.display.flip()
