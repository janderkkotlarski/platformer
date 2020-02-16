import pygame


class Block:

    def __init__(self, width, height, loop):
        self.window_width = width
        self.window_height = height
        self.image = pygame.transform.smoothscale(pygame.image.load("block.png"), (512, 512))
        self.rect = self.image.get_rect()
        self.width = self.rect.right - self.rect.left
        self.height = self.rect.bottom - self.rect.top
        self.position_x = self.window_width / 2
        self.position_y = self.window_height - self.height / 2 - 8
        self.loop = loop

    def positioning(self):
        self.rect.centerx = int(self.position_x)
        self.rect.centery = int(self.position_y)

    def blit(self, screen):
        screen.blit(self.image, self.rect)