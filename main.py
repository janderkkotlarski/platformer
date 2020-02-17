import sys
import numpy
import pygame
import random

from player import Player
from block import Block

pygame.init()

window_size = window_width, window_height = 768, 768
black = 0, 0, 0

screen = pygame.display.set_mode(window_size)

loop = 100

block_width = 128
block_height = 128
block_x = window_width / 2
block_y = window_height / 2

blocks = numpy.array(Block(window_width, window_height, loop, block_width, block_height, random.random()*window_width, random.random()*window_height))

block_number = 10

for count in range(1, block_number + 1):
    blocks = numpy.append(blocks, Block(window_width, window_height, loop, block_width, block_height, random.random()*window_width, random.random()*window_height))

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
