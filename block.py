import pygame


class Block:

    def __init__(self, window_width, window_height, loop, width, height, pos_x, pos_y):
        self.window_width = window_width
        self.window_height = window_height
        self.width = width
        self.height = height
        self.image = pygame.transform.smoothscale(pygame.image.load("block.png"), (width, height))
        self.rect = self.image.get_rect()
        self.position_x = pos_x
        self.position_y = pos_y
        self.loop = loop

    def positioning(self):
        self.rect.centerx = int(self.position_x)
        self.rect.centery = int(self.position_y)

    def blit(self, screen):
        screen.blit(self.image, self.rect)

    def resize(self, width, height):
        self.width = width
        self.height = height
        self.image = pygame.transform.smoothscale(pygame.image.load("block.png"), (width, height))
        self.rect = self.image.get_rect()

    def boundary(self):
        if self.position_x < 0:
            self.position_x += self.window_width

        if self.position_x > self.window_width:
            self.position_x -= self.window_width

        if self.position_y < 0:
            self.position_y += self.window_height

        if self.position_y > self.window_height:
            self.position_y -= self.window_height
