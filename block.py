import pygame
import random
import math


class Block:

    def __init__(self, window_length, loop, length, pos_x, pos_y):
        self.window_length = window_length
        self.length = length
        self.image = pygame.transform.smoothscale(pygame.image.load("block.png"), (int(length), int(length)))
        self.rect = self.image.get_rect()
        self.position_x = pos_x
        self.position_y = pos_y
        self.factor = window_length / 768
        self.passed = 0
        self.loop = loop
        self.speed_z = 0.025 * self.factor
        self.theta = random.random() * 2 * math.pi
        self.phi = 0
        self.speed_x = self.speed_z * math.sin(self.theta)
        self.speed_y = self.speed_z * math.cos(self.theta)

    def positioning(self):
        self.rect.centerx = int(self.position_x)
        self.rect.centery = int(self.position_y)

    def blit(self, screen):
        screen.blit(self.image, self.rect)

    def resize(self, length):
        self.length = length
        self.image = pygame.transform.smoothscale(pygame.image.load("block.png"), (length, length))
        self.rect = self.image.get_rect()

    def boundary(self):
        if self.position_x < 0:
            self.position_x += self.window_length

        if self.position_x > self.window_length:
            self.position_x -= self.window_length

        if self.position_y < 0:
            self.position_y += self.window_length

        if self.position_y > self.window_length:
            self.position_y -= self.window_length

    def set_passed(self, passed):
        self.passed = passed

    def randomove(self):
        self.position_x += self.passed * self.speed_x / self.loop
        self.position_y += self.passed * self.speed_y / self.loop
        self.phi += 0.00005 * math.pi * 2 * random.random()
        psi = self.theta + 0.5 * math.pi * math.sin(self.phi)
        self.speed_x = self.speed_z * math.sin(psi)
        self.speed_y = self.speed_z * math.cos(psi)