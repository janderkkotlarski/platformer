import pygame


class Player:

    def __init__(self, window_length, loop, length):
        self.window_length = window_length
        self.length = length
        self.image = pygame.transform.smoothscale(pygame.image.load("player.png"), (int(length), int(length)))
        self.rect = self.image.get_rect()
        self.delta_x = 0
        self.delta_y = 0
        self.position_x = self.window_length/2
        self.position_y = self.window_length - self.length/2
        self.speed_x = 0
        self.speed_y = 0
        self.factor = window_length / 768
        self.move_speed_x = 0.3 * self.factor
        self.gravity = 0.001 * self.factor
        self.drag = 0.985
        self.jump_speed = -1.1 * self.factor
        self.jumped = False
        self.glue_field = 0.05 * self.factor
        self.drop = 0.2 * self.factor
        self.move_right = False
        self.move_left = False
        self.move_jump = False
        self.move_drop = False
        self.passed = 0
        self.loop = loop

    def set_passed(self, passed):
        self.passed = passed

    def keyboard(self):
        self.move_right = False
        self.move_left = False
        self.move_jump = False
        self.move_drop = False

        keys = pygame.key.get_pressed()

        if keys[pygame.K_RIGHT]:
            self.move_right = True

        if keys[pygame.K_LEFT]:
            self.move_left = True

        if keys[pygame.K_UP] and not self.jumped:
            self.move_jump = True
            self.jumped = True

        if keys[pygame.K_DOWN]:
            self.move_drop = True
            self.move_right = True
            self.move_left = True

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
        if self.position_y >= self.window_length - self.length / 2:
            self.speed_y = 0
            self.position_y = self.window_length - self.length / 2
            if not pygame.key.get_pressed()[pygame.K_UP]:
                self.jumped = False
                self.move

    def collide_against_top(self, block, delta_x_y_plus, delta_y_x_plus, delta_y_x_minus):
        if (self.position_y + self.length / 2 + self.delta_y >= block.position_y - block.length / 2 - self.glue_field) and \
                (self.position_y + self.length / 2 + self.delta_y <= block.position_y) and\
                (delta_x_y_plus <= delta_y_x_plus) and (delta_x_y_plus <= -delta_y_x_minus):
            self.speed_y = 0
            self.position_y = block.position_y - self.delta_y - (block.length + self.length) / 2
            if not pygame.key.get_pressed()[pygame.K_UP]:
                self.jumped = False

    def collide_against_bottom(self, block, delta_x_y_minus, delta_y_x_plus, delta_y_x_minus):

        if (self.position_y - self.length / 2 + self.delta_y <= block.position_y + block.length / 2 + self.glue_field) and \
                (self.position_y - self.length / 2 + self.delta_y >= block.position_y) and \
                (delta_x_y_minus > delta_y_x_minus) and (delta_x_y_minus > -delta_y_x_plus):
            self.speed_y = 0
            self.position_y = block.position_y - self.delta_y + (block.length + self.length) / 2
            self.jumped = True
            if self.move_drop:
                self.speed_y = self.move_speed_x
                self.position_y += self.drop

    def collide_against_right(self, block, delta_x_y_plus, delta_x_y_minus, delta_y_x_minus):

        if (self.position_x - self.length/2 + self.delta_x <= block.position_x + block.length/2 + self.glue_field) and \
                (self.position_x - self.length / 2 + self.delta_x >= block.position_x) and \
                (delta_x_y_minus <= delta_y_x_minus) and (delta_x_y_plus > -delta_y_x_minus):
            self.speed_x = 0
            self.position_x = block.position_x - self.delta_x + (block.length + self.length)/2
            self.jumped = True
            if (self.speed_y <= 0) and (not pygame.key.get_pressed()[pygame.K_UP]):
                self.jumped = False

    def collide_against_left(self, block, delta_x_y_plus, delta_x_y_minus, delta_y_x_plus):

        if (self.position_x + self.length/2 + self.delta_x >= block.position_x - block.length/2 + self.glue_field) and \
                (self.position_x + self.length / 2 + self.delta_x <= block.position_x) and \
                (delta_x_y_plus > delta_y_x_plus) and (delta_x_y_minus <= -delta_y_x_plus):
            self.speed_x = 0
            self.position_x = block.position_x - self.delta_x - (block.length + self.length)/2
            self.jumped = True
            if (self.speed_y <= 0) and (not pygame.key.get_pressed()[pygame.K_UP]):
                self.jumped = False

    def collide(self, block):

        self.delta_x = 0
        self.delta_y = 0

        if (block.position_x - block.length / 2 <= self.length / 2) and\
                (self.position_x >= self.window_length - self.length / 2):
            self.delta_x += -self.window_length

        if (block.position_x + block.length / 2 >= self.window_length - self.length / 2) and\
                (self.position_x <= self.length / 2):
            self.delta_x += self.window_length

        if (block.position_y - block.length / 2 <= self.length / 2) and \
                (self.position_y >= self.window_length - self.length / 2):
            self.delta_y += -self.window_length

        if (block.position_y + block.length / 2 >= self.window_length - self.length / 2) and \
                (self.position_y <= self.length / 2):
            self.delta_y += self.window_length

        delta_x_y_plus = block.length*(self.position_y + self.length / 2 + self.delta_y - block.position_y)
        delta_x_y_minus = delta_x_y_plus - block.length*self.length
        delta_y_x_plus = block.length*(self.position_x + self.length / 2 + self.delta_x - block.position_x)
        delta_y_x_minus = delta_y_x_plus - block.length*self.length

        self.collide_against_top(block, delta_x_y_plus, delta_y_x_plus, delta_y_x_minus)
        self.collide_against_bottom(block, delta_x_y_minus, delta_y_x_plus, delta_y_x_minus)
        self.collide_against_right(block, delta_x_y_plus, delta_x_y_minus, delta_y_x_minus)
        self.collide_against_left(block, delta_x_y_plus, delta_x_y_minus, delta_y_x_plus)

    def dragging(self):
        self.speed_x *= pow(self.drag, 1.0/self.loop)
        self.speed_y *= pow(self.drag, 1.0/self.loop)

    def boundary(self):
        if self.position_x < 0:
            self.position_x += self.window_length

        if self.position_x > self.window_length:
            self.position_x -= self.window_length

        if self.position_y < 0:
            self.position_y += self.window_length

        if self.position_y > self.window_length:
            self.position_y -= self.window_length

    def multi_blit(self, screen):
        for pos_y in range(-1, 2):
            for pos_x in range(-1, 2):
                player_rect = self.rect
                player_rect.centerx = int(self.position_x + pos_x * self.window_length)
                player_rect.centery = int(self.position_y + pos_y * self.window_length)
                screen.blit(self.image, player_rect)