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

    grid_amount = 10

    grid_length = window_length / grid_amount

    player_number = 4

    x_avoid = random.randint(0, grid_amount - 1)
    y_avoid = random.randint(0, grid_amount - 1)

    blockz = [Block(window_length, loop, grid_length, (0.5 + x_avoid) * grid_length, (0.5 + y_avoid) * grid_length)]

    for y_pos in range(0, grid_amount):
        for x_pos in range(0, grid_amount):
            if (x_pos != x_avoid or y_pos != y_avoid) and\
                    (random.randint(1, 10) == 1) and\
                    (len(blockz) < 10):
                blockz.append(
                    Block(window_length, loop, grid_length, (0.5 + x_pos) * grid_length, (0.5 + y_pos) * grid_length))

    blocks = numpy.array(blockz)

    x_avoid = random.randint(0, grid_amount - 1)
    y_avoid = random.randint(0, grid_amount - 1)

    player_id = 0

    playerz = [Player(window_length, loop, 0.5 * grid_length, (0.5 + x_avoid) * grid_length,
                                 (0.5 + y_avoid) * grid_length, player_id)]

    for count in range(1, player_number):
        same_x = True

        while same_x:
            same_x = False

            x_avoid_new = random.randint(0, grid_amount - 1)
            y_avoid = random.randint(0, grid_amount - 1)

            for player in playerz:
                if round((player.position_x / grid_length) - 0.5) == x_avoid_new:
                    same_x = True

        player_id += 1

        playerz.append(Player(window_length, loop, 0.5 * grid_length,
                               (0.5 + x_avoid_new) * grid_length, (0.5 + y_avoid) * grid_length,
                               player_id))

    players = numpy.array(playerz)

    for player in players:
        player.set_keys()

    clock = pygame.time.Clock()

    game_loop = True

    while game_loop:
        passed = clock.tick(loop)

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
                block.randirection()
                block.move()
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
