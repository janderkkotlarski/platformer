import sys
import numpy
import pygame

from player import Player
from block import Block

pygame.init()

size = width, height = 768, 768
speed = [0, 0]
black = 0, 0, 0

screen = pygame.display.set_mode(size)

loop = 100

block = Block(width, height, loop)
player = Player(width, height, loop)

clock = pygame.time.Clock()

while 1:
    passed = clock.tick(100)

    player.set_passed(passed)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                sys.exit()

    for count in range(loop):
        player.fall()
        player.dragging()
        # player.land()

        player.keyboard()

        player.move()

        player.collide(block)

        player.jump()

        player.boundary()

    block.positioning()

    screen.fill(black)

    player.multi_blit(screen)

    block.blit(screen)

    pygame.display.flip()
