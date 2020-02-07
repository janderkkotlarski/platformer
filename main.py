import sys
from typing import List

import pygame

pygame.init()


class Player:

    def __init__(self, right, left, top, bottom, width, height):
        self.window_width = width
        self.window_height = height
        self.width = left - right
        self.height = bottom - top
        self.position_x = self.window_width/2
        self.position_y = self.window_height - self.height/2
        self.speed_x = 0
        self.speed_y = 0
        self.move_speed_x = 0.5
        self.gravity = 0.003
        self.drag = 0.996
        self.dragging = False
        self.jump_speed = -0.4
        self.jumped = True

    def fall(self):
        self.speed_y += self.gravity
        self.position_y += self.speed_y
        if self.position_y >= self.window_height - self.height/2:
            self.speed_y = 0
            self.position_y = self.window_height - self.height/2
            self.jumped = False

    def jump(self):
        if not self.jumped:
            self.speed_y = -2
            self.jumped = True

    def move(self):
        self.position_x += self.speed_x

    def move_right(self):
        self.speed_x = self.move_speed_x;
        self.dragging = True

    def move_left(self):
        self.speed_x = -self.move_speed_x;
        self.dragging = True

    def move_drag(self):
        self.dragging = False

    def move_stop(self):
        self.speed_x = 0

    def dragging_x(self):
        self.speed_x *= self.drag

    def dragging_y(self):
        self.speed_y *= self.drag

    def boundary(self):
        if self.position_x < self.width/2:
            self.position_x = self.width/2
            self.speed_x = 0

        if self.position_x > self.window_width - self.width/2:
            self.position_x = self.window_width - self.width/2
            self.speed_x = 0


pygame.key.set_repeat(1, 1)

size = width, height = 800, 600
speed = [0, 0]
black = 0, 0, 0

screen = pygame.display.set_mode(size)

player_sprite = pygame.image.load("player.png")
player_rect = player_sprite.get_rect()

player = Player(player_rect.right, player_rect.left, player_rect.top, player_rect.bottom, width, height)

while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                sys.exit()
            if event.key == pygame.K_UP:
                player.jump()
            if event.key == pygame.K_RIGHT:
                player.move_right()
            if event.key == pygame.K_LEFT:
                player.move_left()
        else:
            player.move_drag()

    player.fall()
    player.move()

    player.dragging_x()

    player.dragging_y()

    player.boundary()

    player_rect.centerx = int(player.position_x)
    player_rect.centery = int(player.position_y)

    screen.fill(black)
    screen.blit(player_sprite, player_rect)
    pygame.display.flip()
