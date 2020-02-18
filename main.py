import sys
import numpy
import pygame
import random

from player import Player
from block import Block

pygame.init()

window_length = 768

window_size = window_length, window_length
black = 0, 0, 0

screen = pygame.display.set_mode(window_size)

loop = 100

grid_length = window_length / 20

blocks = numpy.array(Block(window_length, loop, 2*grid_length, window_length*random.random(), window_length*random.random()))

block_number = 10

for count in range(1, block_number + 1):
    blocks = numpy.append(blocks, numpy.array(Block(window_length, loop, 2*grid_length, window_length*random.random(), window_length*random.random())))

player = Player(window_length, loop, grid_length)

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

        player.keyboard()

        player.move()

        for block in blocks:
            player.collide(block)

        player.jump()

        for block in blocks:
            block.set_passed(passed)
            block.randomove()
            block.boundary()

        player.boundary()

    screen.fill(black)

    for block in blocks:
        block.positioning()
        block.blit(screen)

    player.multi_blit(screen)

    pygame.display.flip()
