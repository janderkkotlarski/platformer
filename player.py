import pygame


class Player:

    def __init__(self, window_length, loop, length, pos_x, pos_y, identity):
        self.window_length = window_length
        self.length = length
        self.radius = length / 2
        self.image = pygame.transform.smoothscale(pygame.image.load("player.png"), (int(length), int(length)))
        self.rect = self.image.get_rect()
        self.delta_x = 0
        self.delta_y = 0
        self.position_x = pos_x
        self.position_y = pos_y
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
        self.alive = True
        self.passed = 0
        self.loop = loop
        self.identity = identity
        self.key_up = pygame.K_UP
        self.key_down = pygame.K_DOWN
        self.key_right = pygame.K_RIGHT
        self.key_left = pygame.K_LEFT

    def set_passed(self, passed):
        self.passed = passed

    def colorize(self, color):

        image = self.image.copy()

        image.fill((0, 0, 0, 255), None, pygame.BLEND_RGBA_MULT)
        image.fill(color[0:3] + (0,), None, pygame.BLEND_RGBA_ADD)

        return image

    def set_keys(self):

        color = (127, 127, 127)

        if self.identity == 0:
            color = (255, 0, 0)

        if self.identity == 1:
            self.key_up = pygame.K_w
            self.key_down = pygame.K_s
            self.key_right = pygame.K_d
            self.key_left = pygame.K_a
            color = (0, 255, 0)

        if self.identity == 2:
            self.key_up = pygame.K_t
            self.key_down = pygame.K_g
            self.key_right = pygame.K_h
            self.key_left = pygame.K_f
            color = (255, 255, 0)

        if self.identity == 3:
            self.key_up = pygame.K_i
            self.key_down = pygame.K_k
            self.key_right = pygame.K_l
            self.key_left = pygame.K_j
            color = (0, 0, 255)

        self.image = self.colorize(color)

    def keyboard(self):
        if self.alive:
            self.move_right = False
            self.move_left = False
            self.move_jump = False
            self.move_drop = False

            keys = pygame.key.get_pressed()

            if keys[self.key_right]:
                self.move_right = True

            if keys[self.key_left]:
                self.move_left = True

            if keys[self.key_up] and not self.jumped:
                self.move_jump = True
                self.jumped = True

            if keys[self.key_down]:
                self.move_drop = True
                self.move_right = True
                self.move_left = True

    def move(self):
        if self.alive:
            if self.move_right:
                self.speed_x = self.move_speed_x

            if self.move_left:
                self.speed_x = -self.move_speed_x

                if self.move_right:
                    self.speed_x = 0

            self.position_x += self.passed*self.speed_x/self.loop

    def jump(self):
        if self.alive and self.move_jump:
            self.speed_y += self.jump_speed
            self.jumped = True

    def fall(self):
        if self.alive:
            if self.speed_y > 0:
                self.jumped = True

            self.speed_y += self.passed*self.gravity/self.loop
            self.position_y += self.passed*self.speed_y/self.loop

    def collide_against_top(self, block, delta_x_y_plus, delta_y_x_plus, delta_y_x_minus):
        if (self.position_y + self.radius + self.delta_y >= block.position_y - block.radius - self.glue_field) and \
                (self.position_y + self.radius + self.delta_y <= block.position_y) and\
                (delta_x_y_plus <= delta_y_x_plus) and (delta_x_y_plus <= -delta_y_x_minus):
            self.speed_y = 0
            self.position_y = block.position_y - self.delta_y - block.radius - self.radius
            if not pygame.key.get_pressed()[self.key_up]:
                self.jumped = False

    def collide_against_bottom(self, block, delta_x_y_minus, delta_y_x_plus, delta_y_x_minus):
        if (self.position_y - self.radius + self.delta_y <= block.position_y + block.radius + self.glue_field) and \
                (self.position_y - self.radius + self.delta_y >= block.position_y) and \
                (delta_x_y_minus > delta_y_x_minus) and (delta_x_y_minus > -delta_y_x_plus):
            self.speed_y = 0
            self.position_y = block.position_y - self.delta_y + block.radius + self.radius
            self.jumped = True
            if self.move_drop:
                self.speed_y = self.move_speed_x
                self.position_y += self.drop

    def collide_against_right(self, block, delta_x_y_plus, delta_x_y_minus, delta_y_x_minus):
        if (self.position_x - self.radius + self.delta_x <= block.position_x + block.radius + self.glue_field) and \
                (self.position_x - self.radius + self.delta_x >= block.position_x) and \
                (delta_x_y_minus <= delta_y_x_minus) and (delta_x_y_plus > -delta_y_x_minus):
            self.speed_x = 0
            self.position_x = block.position_x - self.delta_x + block.radius + self.radius
            self.jumped = True
            if (self.speed_y <= 0) and (not pygame.key.get_pressed()[self.key_up]):
                self.jumped = False

    def collide_against_left(self, block, delta_x_y_plus, delta_x_y_minus, delta_y_x_plus):
        if (self.position_x + self.radius + self.delta_x >= block.position_x - block.radius + self.glue_field) and \
                (self.position_x + self.radius + self.delta_x <= block.position_x) and \
                (delta_x_y_plus > delta_y_x_plus) and (delta_x_y_minus <= -delta_y_x_plus):
            self.speed_x = 0
            self.position_x = block.position_x - self.delta_x - block.radius - self.radius
            self.jumped = True
            if (self.speed_y <= 0) and (not pygame.key.get_pressed()[self.key_up]):
                self.jumped = False

    def collide(self, block):
        if self.alive:
            self.delta_x = 0
            self.delta_y = 0

            # Collide against left of block
            if (block.position_x - block.radius <= self.position_x + self.radius - self.window_length) and\
                    (self.position_x >= self.window_length - self.radius):
                self.delta_x += -self.window_length

            if (block.position_x + block.radius >= self.position_x - self.radius + self.window_length) and\
                    (self.position_x <= self.radius):
                self.delta_x += self.window_length

            if (block.position_y - block.radius <= self.position_y + self.radius - self.window_length) and \
                    (self.position_y >= self.window_length - self.radius):
                self.delta_y += -self.window_length

            if (block.position_y + block.radius >= self.position_y - self.radius + self.window_length) and \
                    (self.position_y <= self.radius):
                self.delta_y += self.window_length

            # self.delta_x = 0
            # self.delta_y = 0

            delta_x_y_plus = block.length*(self.position_y + self.radius + self.delta_y - block.position_y)
            delta_x_y_minus = delta_x_y_plus - block.length*self.length
            delta_y_x_plus = block.length*(self.position_x + self.radius + self.delta_x - block.position_x)
            delta_y_x_minus = delta_y_x_plus - block.length*self.length

            self.collide_against_top(block, delta_x_y_plus, delta_y_x_plus, delta_y_x_minus)
            self.collide_against_bottom(block, delta_x_y_minus, delta_y_x_plus, delta_y_x_minus)
            self.collide_against_right(block, delta_x_y_plus, delta_x_y_minus, delta_y_x_minus)
            self.collide_against_left(block, delta_x_y_plus, delta_x_y_minus, delta_y_x_plus)

    def collide_other_top(self, player, delta_x_y_plus, delta_y_x_plus, delta_y_x_minus):
        if (self.position_y + self.radius + self.delta_y >= player.position_y - player.radius - self.glue_field) and \
                (self.position_y + self.radius + self.delta_y <= player.position_y) and\
                (delta_x_y_plus <= delta_y_x_plus) and (delta_x_y_plus <= -delta_y_x_minus):
            self.speed_y = 0

            average_y = (self.position_y + player.position_y) / 2

            self.position_y = average_y - self.radius
            player.position_y = average_y + player.radius

            player.alive = False

    def collide_other_bottom(self, player, delta_x_y_minus, delta_y_x_plus, delta_y_x_minus):
        if (self.position_y - self.radius + self.delta_y <= player.position_y + player.radius + self.glue_field) and \
                (self.position_y - self.radius + self.delta_y >= player.position_y) and \
                (delta_x_y_minus > delta_y_x_minus) and (delta_x_y_minus > -delta_y_x_plus):
            self.speed_y = 0

            average_y = (self.position_y + player.position_y) / 2

            self.position_y = average_y + self.radius
            player.position_y = average_y - player.radius

            self.alive = False

    def collide_other_right(self, player, delta_x_y_plus, delta_x_y_minus, delta_y_x_minus):
        if (self.position_x - self.radius + self.delta_x <= player.position_x + player.radius + self.glue_field) and \
                (self.position_x - self.radius + self.delta_x >= player.position_x) and \
                (delta_x_y_minus <= delta_y_x_minus) and (delta_x_y_plus > -delta_y_x_minus):
            self.speed_x = 0
            player.speed_x = 0

            average_x = (self.position_x + player.position_x) / 2

            self.position_x = average_x + self.radius
            player.position_x = average_x - player.radius

    def collide_other_left(self, player, delta_x_y_plus, delta_x_y_minus, delta_y_x_plus):
        if (self.position_x + self.radius + self.delta_x >= player.position_x - player.radius + self.glue_field) and \
                (self.position_x + self.radius + self.delta_x <= player.position_x) and \
                (delta_x_y_plus > delta_y_x_plus) and (delta_x_y_minus <= -delta_y_x_plus):
            self.speed_x = 0
            player.speed_x = 0

            average_x = (self.position_x + player.position_x) / 2

            self.position_x = average_x - self.radius
            player.position_x = average_x + player.radius

    def collide_other(self, player):
        if self.alive and player.alive:
            self.delta_x = 0
            self.delta_y = 0

            if (player.position_x - player.radius <= self.radius) and \
                    (self.position_x >= self.window_length - self.radius):
                self.delta_x += -self.window_length

            if (player.position_x + player.radius >= self.window_length - self.radius) and \
                    (self.position_x <= self.radius):
                self.delta_x += self.window_length

            if (player.position_y - player.radius <= self.radius) and \
                    (self.position_y >= self.window_length - self.radius):
                self.delta_y += -self.window_length

            if (player.position_y + player.radius >= self.window_length - self.radius) and \
                    (self.position_y <= self.radius):
                self.delta_y += self.window_length

            delta_x_y_plus = player.length * (self.position_y + self.radius + self.delta_y - player.position_y)
            delta_x_y_minus = delta_x_y_plus - player.length * self.length
            delta_y_x_plus = player.length * (self.position_x + self.radius + self.delta_x - player.position_x)
            delta_y_x_minus = delta_y_x_plus - player.length * self.length

            self.collide_other_top(player, delta_x_y_plus, delta_y_x_plus, delta_y_x_minus)
            self.collide_other_bottom(player, delta_x_y_minus, delta_y_x_plus, delta_y_x_minus)
            self.collide_other_right(player, delta_x_y_plus, delta_x_y_minus, delta_y_x_minus)
            self.collide_other_left(player, delta_x_y_plus, delta_x_y_minus, delta_y_x_plus)

    def dragging(self):
        if self.alive:
            self.speed_x *= pow(self.drag, 1.0/self.loop)
            self.speed_y *= pow(self.drag, 1.0/self.loop)

    def boundary(self):
        if self.alive:
            if self.position_x < 0:
                self.position_x += self.window_length

            if self.position_x > self.window_length:
                self.position_x -= self.window_length

            if self.position_y < 0:
                self.position_y += self.window_length

            if self.position_y > self.window_length:
                self.position_y -= self.window_length

    def multi_blit(self, screen):
        if self.alive:
            for pos_y in range(-1, 2):
                for pos_x in range(-1, 2):
                    self_rect = self.rect
                    self_rect.centerx = int(self.position_x + pos_x * self.window_length)
                    self_rect.centery = int(self.position_y + pos_y * self.window_length)
                    screen.blit(self.image, self_rect)