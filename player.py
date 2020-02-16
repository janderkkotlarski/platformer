import pygame


class Player:

    def __init__(self, width, height, loop):
        self.window_width = width
        self.window_height = height
        self.image = pygame.transform.smoothscale(pygame.image.load("player.png"), (32, 32))
        self.rect = self.image.get_rect()
        self.width = self.rect.right - self.rect.left
        self.height = self.rect.bottom - self.rect.top
        self.delta_x = 0
        self.delta_y = 0
        self.position_x = self.window_width/2
        self.position_y = self.window_height - self.height/2
        self.speed_x = 0
        self.speed_y = 0
        self.move_speed_x = 0.3
        self.gravity = 0.001
        self.drag = 0.985
        self.jump_speed = -1.1
        self.jumped = False
        self.move_right = False
        self.move_left = False
        self.move_jump = False
        self.passed = 0
        self.loop = loop

    def set_passed(self, passed):
        self.passed = passed

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

        self.position_x += self.passed*self.speed_x/self.loop

    def jump(self):
        if self.move_jump:
            self.speed_y += self.jump_speed
            self.jumped = True

    def fall(self):
        if self.speed_y > 0:
            self.jumped = True

        self.speed_y += self.passed*self.gravity/self.loop
        self.position_y += self.passed*self.speed_y/self.loop

    def land(self):
        if self.position_y >= self.window_height - self.height / 2:
            self.speed_y = 0
            self.position_y = self.window_height - self.height / 2
            if not pygame.key.get_pressed()[pygame.K_UP]:
                self.jumped = False
                self.move

    def collide_against_top(self, block, delta_x_y_plus, delta_y_x_plus, delta_y_x_minus):
        if (self.position_y + self.height / 2 + self.delta_y >= block.position_y - block.height / 2 - 0.01) and \
                (self.position_y + self.height / 2 + self.delta_y <= block.position_y) and\
                (delta_x_y_plus <= delta_y_x_plus) and (delta_x_y_plus <= -delta_y_x_minus):
            self.speed_y = 0
            self.position_y = block.position_y - self.delta_y - (block.height + self.height) / 2
            if not pygame.key.get_pressed()[pygame.K_UP]:
                self.jumped = False

    def collide_against_bottom(self, block, delta_x_y_minus, delta_y_x_plus, delta_y_x_minus):

        if (self.position_y - self.height / 2 + self.delta_y <= block.position_y + block.height / 2 + 0.05) and \
                (self.position_y - self.height / 2 + self.delta_y >= block.position_y) and \
                (delta_x_y_minus > delta_y_x_minus) and (delta_x_y_minus > -delta_y_x_plus):
            self.speed_y = 0
            self.position_y = block.position_y - self.delta_y + (block.height + self.height) / 2
            self.jumped = True

    def collide_against_right(self, block, delta_x_y_plus, delta_x_y_minus, delta_y_x_minus):

        if (self.position_x - self.width/2 + self.delta_x <= block.position_x + block.width/2 + 0.05) and \
                (self.position_x - self.width / 2 + self.delta_x >= block.position_x) and \
                (delta_x_y_minus <= delta_y_x_minus) and (delta_x_y_plus > -delta_y_x_minus):
            self.speed_x = 0
            self.position_x = block.position_x - self.delta_x + (block.width + self.width)/2
            self.jumped = True
            if (self.speed_y <= 0) and (not pygame.key.get_pressed()[pygame.K_UP]):
                self.jumped = False

    def collide_against_left(self, block, delta_x_y_plus, delta_x_y_minus, delta_y_x_plus):

        if (self.position_x + self.width/2 + self.delta_x >= block.position_x - block.width/2 + 0.05) and \
                (self.position_x + self.width / 2 + self.delta_x <= block.position_x) and \
                (delta_x_y_plus > delta_y_x_plus) and (delta_x_y_minus <= -delta_y_x_plus):
            self.speed_x = 0
            self.position_x = block.position_x - self.delta_x - (block.width + self.width)/2
            self.jumped = True
            if (self.speed_y <= 0) and (not pygame.key.get_pressed()[pygame.K_UP]):
                self.jumped = False

    def collide(self, block):

        self.delta_x = 0
        self.delta_y = 0

        if (block.position_x - block.width / 2 <= self.width / 2) and\
                (self.position_x >= self.window_width - self.width / 2):
            self.delta_x += -self.window_width

        if (block.position_x + block.width / 2 >= self.window_width - self.width / 2) and\
                (self.position_x <= self.width / 2):
            self.delta_x += self.window_width

        if (block.position_y - block.height / 2 <= self.height / 2) and \
                (self.position_y >= self.window_height - self.height / 2):
            self.delta_y += -self.window_height

        if (block.position_y + block.height / 2 >= self.window_height - self.height / 2) and \
                (self.position_y <= self.height / 2):
            self.delta_y += self.window_height

        delta_x_y_plus = block.width*(self.position_y + self.height / 2 + self.delta_y - block.position_y)
        delta_x_y_minus = delta_x_y_plus - block.width*self.height
        delta_y_x_plus = block.height*(self.position_x + self.width / 2 + self.delta_x - block.position_x)
        delta_y_x_minus = delta_y_x_plus - block.height*self.width

        self.collide_against_top(block, delta_x_y_plus, delta_y_x_plus, delta_y_x_minus)
        self.collide_against_bottom(block, delta_x_y_minus, delta_y_x_plus, delta_y_x_minus)
        self.collide_against_right(block, delta_x_y_plus, delta_x_y_minus, delta_y_x_minus)
        self.collide_against_left(block, delta_x_y_plus, delta_x_y_minus, delta_y_x_plus)

    def dragging(self):
        self.speed_x *= pow(self.drag, 1.0/self.loop)
        self.speed_y *= pow(self.drag, 1.0/self.loop)

    def boundary(self):
        if self.position_x < 0:
            self.position_x += self.window_width

        if self.position_x > self.window_width:
            self.position_x -= self.window_width

        if self.position_y < 0:
            self.position_y += self.window_height

        if self.position_y > self.window_height:
            self.position_y -= self.window_height

    def multi_blit(self, screen):
        for pos_y in range(-1, 2):
            for pos_x in range(-1, 2):
                player_rect = self.rect
                player_rect.centerx = int(self.position_x + pos_x * self.window_width)
                player_rect.centery = int(self.position_y + pos_y * self.window_height)
                screen.blit(self.image, player_rect)