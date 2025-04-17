import pygame
import random

pygame.init()

# Enemy uses pygame's built-in Sprite class so it can be grouped and drawn easily
class Enemy(pygame.sprite.Sprite):  # Sprite class used here, carries over own functionality (draw etc...)
    def __init__(self, x, y, width=30, height=30):
        super().__init__()

        # load enemy animation frames (with repeated idle frames to slow the animation slightly)
        self.frames = [pygame.image.load(x) for x in ["Assets/Enemy1.png", 
                                                      "Assets/Enemy1.png", 
                                                      "Assets/Enemy1.png", 
                                                      "Assets/Enemy1.png", 
                                                      "Assets/EnemyFrame1.png", 
                                                      "Assets/EnemyFrame2.png", 
                                                      "Assets/EnemyFrame3.png"]]

        # scale all frames to match enemy dimensions
        self.frames = [pygame.transform.scale(x, (width, height)) for x in self.frames]

        # start at a random animation frame so enemies don’t all move in sync
        self.animation_index = random.randint(0, len(self.frames) - 1)
        self.image = self.frames[self.animation_index]
        self.timer = 0

        # set up the enemy's position and size using a rectangle
        self.rect = self.image.get_rect(topleft=(x, y))

    def animate(self, delta_time):
        self.timer += delta_time

        # only update frame every ~1/15 seconds
        if self.timer < (1 / 15):
            return

        # loop animation frames
        self.timer = 0
        self.animation_index = (self.animation_index + 1) % len(self.frames)
        self.image = self.frames[self.animation_index]


class Player:
    def __init__(self, rect, speed, is_jumping, on_ground, is_paused, jump_count, volume):
        self.rect = rect
        self.spawn_point = (self.rect.x, self.rect.y)  # used to reset after death
        self.colour = '#0A9B9A'
        self.velocity = [0, 0]  # x and y movement speed
        self.speed = speed
        self.is_jumping = is_jumping
        self.on_ground = on_ground
        self.jump_count = jump_count
        self.tile_list = []  # tiles used for collision detection
        self.is_paused = is_paused
        self.volume = volume
        self.end = False

    def update_tile_list(self, new):
        self.tile_list = new

    # modify the velocity directly (used in scripts or events)
    def animate(self, x, y):
        self.velocity[0] += x
        self.velocity[1] += y

    def draw(self, screen):
        pygame.draw.rect(screen, self.colour, self.rect)

    # checks for game over conditions — falling, touching hazards, or reaching the goal
    def game_over(self, height, enemies):
        if self.rect.y > height:
            return -1  # fell off screen
        for tile in self.tile_list:
            if tile.rect.colliderect(self.rect.x, self.rect.y + self.velocity[1], self.rect.width, self.rect.height):
                if tile.kind == 2:  # lava tile
                    return -1
                elif tile.kind == 4:  # goal tile
                    return 1
        # check for enemy collisions
        if pygame.sprite.spritecollide(self, enemies, False):
            return -1

    # handles all X and Y collision logic with the world
    def check_collisions(self):
        for tile in self.tile_list:
            if tile.kind != 4:  # ignore goal tile for collisions
                # check for horizontal collisions (left side)
                if tile.rect.colliderect(self.rect.x + self.velocity[0],
                                         self.rect.y + self.rect.height / 4,
                                         self.rect.width / 2,
                                         self.rect.height / 2):
                    self.velocity[0] += 10
                # check for horizontal collisions (right side)
                elif tile.rect.colliderect(self.rect.x + self.velocity[0] + self.rect.width / 2,
                                           self.rect.y + self.rect.height / 4,
                                           self.rect.width / 2,
                                           self.rect.height / 2):
                    self.velocity[0] -= 10
                # check for vertical collisions (top and bottom)
                elif tile.rect.colliderect(self.rect.x,
                                           self.rect.y + self.velocity[1],
                                           self.rect.width,
                                           self.rect.height):
                    if self.velocity[1] < 0:
                        # hitting a ceiling
                        self.rect.top = tile.rect.bottom + 0.1
                        self.velocity[1] = 0
                    elif self.velocity[1] >= 0:
                        # landing on ground
                        self.rect.bottom = tile.rect.top - 0.1
                        self.velocity[1] = 0

    def update(self):
        if not self.is_paused:
            # check for and resolve collisions
            for _ in range(1):  # stub for potential loop expansion
                self.check_collisions()

            # apply velocity to position
            self.rect.x += self.velocity[0]
            self.rect.y += self.velocity[1]

            # slow down X movement, simulate friction
            self.velocity[0] *= 0.001
            # apply gravity
            self.velocity[1] += 0.6

    def check_input(self):
        if not self.is_paused:
            keys = pygame.key.get_pressed()

            # horizontal movement
            if keys[pygame.K_a]:
                self.velocity[0] = -self.speed
            if keys[pygame.K_d]:
                self.velocity[0] = self.speed

            # jump input
            if (keys[pygame.K_SPACE] or keys[pygame.K_w]) and self.is_on_ground():
                self.velocity[1] -= 10
                jump_sfx = pygame.mixer.Sound("Sounds/Jump.wav")
                jump_sfx.set_volume(self.volume)
                if self.volume > 0.04:
                    jump_sfx.play()

        # pause button
        if keys[pygame.K_ESCAPE]:
            self.is_paused = True

    def is_on_ground(self):
        # checks if the player is standing on any tile (prevents infinite jumping)
        for tile in self.tile_list:
            if tile.rect.colliderect(self.rect.x, self.rect.y + self.velocity[1], self.rect.width, self.rect.height):
                if self.velocity[1] >= 0:
                    return True
        return False
