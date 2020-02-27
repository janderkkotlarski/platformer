import pygame
import random
import math


class Block:

    def __init__(self, window_length, loop, length, pos_x, pos_y):
        self.window_length = window_length
        self.length = length
        self.radius = length / 2
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
        self.speed_x = 0
        self.speed_y = 0

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

    def randirection(self):
        if abs(self.position_x % self.length - self.radius) <= self.radius / (self.loop * self.loop) and \
                abs(self.position_y % self.length - self.radius) <= self.radius / (self.loop * self.loop):
            self.position_x = round((self.position_x - self.radius) / self.length) * self.length + self.radius
            self.position_y = round((self.position_y - self.radius) / self.length) * self.length + self.radius

            randir = random.randint(1, 4)

            if randir == 1:
                self.speed_x = self.speed_z
                self.speed_y = 0
            if randir == 2:
                self.speed_x = 0
                self.speed_y = self.speed_z
            if randir == 3:
                self.speed_x = -self.speed_z
                self.speed_y = 0
            if randir == 4:
                self.speed_x = 0
                self.speed_y = -self.speed_z


    def move(self):
        self.position_x += self.passed * self.speed_x / self.loop
        self.position_y += self.passed * self.speed_y / self.loop

    def multi_blit(self, screen):
        for pos_y in range(-1, 2):
            for pos_x in range(-1, 2):
                self_rect = self.rect
                self_rect.centerx = int(self.position_x + pos_x * self.window_length)
                self_rect.centery = int(self.position_y + pos_y * self.window_length)
                screen.blit(self.image, self_rect)