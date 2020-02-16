import sys
import numpy
import pygame

from player import Player
from block import Block

pygame.init()

window_size = window_width, window_height = 768, 768
black = 0, 0, 0

screen = pygame.display.set_mode(window_size)

loop = 100

block_width = 256
block_height = 256
block_x = window_width / 2
block_y = window_height / 2

block = Block(window_width, window_height, loop, block_width, block_height, block_x, block_y)
player = Player(window_width, window_height, loop)

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
