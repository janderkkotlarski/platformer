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

while 1:

    loop = 100

    grid_length = window_length / 20

    player_number = 4

    blocks = numpy.array(Block(window_length, loop, 2*grid_length, grid_length, grid_length))

    block_number = 10

    for count in range(1, block_number + 1):
        blocks = numpy.append(blocks, numpy.array(Block(window_length, loop, 2*grid_length, window_length*random.random(), window_length*random.random())))

    players = numpy.array(Player(window_length, loop, grid_length, window_length*random.random(), window_length*random.random(), 0))

    for count in range(1, player_number):
        players = numpy.append(players, numpy.array(Player(window_length, loop, grid_length, window_length*random.random(), window_length*random.random(), count)))

    for player in players:
        player.set_keys()

    clock = pygame.time.Clock()

    game_loop = True

    while game_loop:
        passed = clock.tick(100)

        for player in players:
            player.set_passed(passed)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    sys.exit()

                if event.key == pygame.K_RETURN:
                    game_loop = False

        for count in range(loop):
            for player in players:
                player.fall()
                player.dragging()

                player.keyboard()

                player.move()

                for block in blocks:
                    player.collide(block)

            for count_2 in range(0, player_number - 1):
                for count_3 in range(count_2 + 1, player_number):
                    players[count_2].collide_other(players[count_3])

            for player in players:
                player.jump()

            for block in blocks:
                block.set_passed(passed)
                # block.randomove()
                block.boundary()

            for player in players:
                player.boundary()

        screen.fill(black)

        for block in blocks:
            block.positioning()
            block.multi_blit(screen)

        for player in players:
            player.multi_blit(screen)

        pygame.display.flip()
