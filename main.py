import sys
import numpy
import pygame

pygame.init()

class Block:

    def __init__(self, width, height):
        self.window_width = width
        self.window_height = height
        self.image = pygame.transform.smoothscale(pygame.image.load("block.png"), (32, 32))
        self.rect = self.image.get_rect()
        self.width = self.rect.right - self.rect.left
        self.height = self.rect.bottom - self.rect.top
        self.position_x = self.window_width / 2
        self.position_y = self.window_height / 2

    def positioning(self):
        self.rect.centerx = int(self.position_x)
        self.rect.centery = int(self.position_y)

class Player:

    def __init__(self, width, height):
        self.window_width = width
        self.window_height = height
        self.image = pygame.transform.smoothscale(pygame.image.load("player.png"), (32, 32))
        self.rect = self.image.get_rect()
        self.width = self.rect.right - self.rect.left
        self.height = self.rect.bottom - self.rect.top
        self.position_x = self.window_width/2
        self.position_y = self.window_height - self.height/2
        self.speed_x = 0
        self.speed_y = 0
        self.move_speed_x = 0.3
        self.gravity = 0.001
        self.drag = 0.998
        self.jump_speed = -1.5
        self.jumped = False
        self.move_right = False
        self.move_left = False
        self.move_jump = False

    def keyboard(self):
        self.move_right = False
        self.move_left = False
        self.move_jump = False

        keys = pygame.key.get_pressed()

        if keys[pygame.K_RIGHT]:
            self.move_right = True

        if keys[pygame.K_LEFT]:
            self.move_left = True

        if keys[pygame.K_UP] and not self.jumped:
            self.move_jump = True
            self.jumped = True

    def move(self):
        if self.move_right:
            self.speed_x = self.move_speed_x

        if self.move_left:
            self.speed_x = -self.move_speed_x

            if self.move_right:
                self.speed_x = 0

        self.position_x += self.speed_x

    def jump(self):
        if self.move_jump:
            self.speed_y = self.jump_speed
            self.jumped = True

    def fall(self):
        self.speed_y += self.gravity
        self.position_y += self.speed_y

    def land(self):
        if self.position_y >= self.window_height - self.height / 2:
            self.speed_y = 0
            self.position_y = self.window_height - self.height / 2
            if not  pygame.key.get_pressed()[pygame.K_UP]:
                self.jumped = False

    def dragging(self):
        self.speed_x *= self.drag
        self.speed_y *= self.drag

    def boundary(self):
        if self.position_x < self.width/2:
            self.position_x = self.width/2
            self.speed_x = 0

        if self.position_x > self.window_width - self.width/2:
            self.position_x = self.window_width - self.width/2
            self.speed_x = 0

    def collide_down(self, block):


    def positioning(self):
        self.rect.centerx = int(self.position_x)
        self.rect.centery = int(self.position_y)


#  pygame.key.set_repeat(1, 1)

size = width, height = 800, 600
speed = [0, 0]
black = 0, 0, 0

screen = pygame.display.set_mode(size)

block = Block(width, height)
player = Player(width, height)

while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                sys.exit()

    player.fall()
    player.dragging()
    player.land()

    player.keyboard()

    player.move()
    player.jump()

    player.boundary()
    player.positioning()

    block.positioning()

    screen.fill(black)

    screen.blit(player.image, player.rect)
    screen.blit(block.image, block.rect)

    pygame.display.flip()
