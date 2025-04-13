import pygame
import random

pygame.init()


class Enemy(pygame.sprite.Sprite): # Sprite class used here, carries over own functionality (draw etc...)

    def __init__(self, x, y, width=30, height=30):
        super().__init__()
   

        self.frames = [pygame.image.load(x) for x in ["Assets/Enemy1.png", 
                                                      "Assets/Enemy1.png", 
                                                      "Assets/Enemy1.png", 
                                                      "Assets/Enemy1.png", 
                                                      "Assets/EnemyFrame1.png", 
                                                      "Assets/EnemyFrame2.png", 
                                                      "Assets/EnemyFrame3.png"]]

        self.frames = [pygame.transform.scale(x, (width, height)) for x in self.frames]
        self.animation_index = random.randint(0, len(self.frames) - 1)
        self.image = self.frames[self.animation_index]
        self.timer = 0

        self.rect = self.image.get_rect(topleft=(x, y))

    def animate(self, delta_time):
        self.timer += delta_time

        if self.timer < (1/15):
            return 
        
        self.timer = 0
        self.animation_index = (self.animation_index + 1) % len(self.frames)
        self.image = self.frames[self.animation_index]

class Player:
    def __init__(self, rect, speed, is_jumping, on_ground, is_paused, jump_count, volume):
        self.rect = rect
        self.spawn_point = (self.rect.x, self.rect.y)
        self.colour = ('#0A9B9A')
        self.velocity = [0, 0]
        self.speed = speed
        self.is_jumping = is_jumping
        self.on_ground = on_ground
        self.jump_count = jump_count
        self.tile_list = []
        self.is_paused = is_paused
        self.volume = volume
        self.end = False

    def update_tile_list(self, new):
        self.tile_list = new


    # subroutine which animates player
    def animate(self, x, y):
        self.velocity[0] += x
        self.velocity[1] += y


    def draw(self, screen):
        pygame.draw.rect(screen, self.colour, self.rect)


    def game_over(self, height, enemies):
        if self.rect.y > height:
            return -1
        for tile in self.tile_list:
            if tile.rect.colliderect(self.rect.x, self.rect.y + self.velocity[1], self.rect.width, self.rect.height):
                if tile.kind == 2:
                    return -1
                elif tile.kind == 4:
                    return 1
            if pygame.sprite.spritecollide(self, enemies, False):
                return -1


    def check_collisions(self):
        for tile in self.tile_list:
            if tile.kind != 4:
                if tile.rect.colliderect(self.rect.x + self.velocity[0],
                                        self.rect.y + self.rect.height / 4,
                                        self.rect.width / 2,
                                        self.rect.height / 2):
                    self.velocity[0] += 10
                elif tile.rect.colliderect(self.rect.x + self.velocity[0] + self.rect.width / 2,
                                        self.rect.y + self.rect.height / 4,
                                        self.rect.width / 2,
                                        self.rect.height / 2):
                    self.velocity[0] -= 10
                elif tile.rect.colliderect(self.rect.x,
                                        self.rect.y + self.velocity[1],
                                        self.rect.width,
                                        self.rect.height):
                    # jumping upwards / ground below (in pygame speak)
                    if self.velocity[1] < 0:
                        self.rect.top = (tile.rect.bottom + 0.1)
                        self.velocity[1] = 0
                    # falling down / ground above
                    elif self.velocity[1] >= 0:
                        self.rect.bottom = (tile.rect.top - 0.1)
                        self.velocity[1] = 0


    def update(self):
        if not self.is_paused:
            for i in range(1):
                self.check_collisions()

            
            self.rect.x += self.velocity[0]
            self.rect.y += self.velocity[1]

            self.velocity[0] *= 0.001
            self.velocity[1] += 0.6


    def check_input(self):
        if not self.is_paused:
            keys = pygame.key.get_pressed()

            # left and right always active, no restraints
            if keys[pygame.K_a]:  # moving left
                self.velocity[0] = -self.speed
            if keys[pygame.K_d]:  # moving right
                self.velocity[0] = self.speed

            if (keys[pygame.K_SPACE] or keys[pygame.K_w]) and self.is_on_ground():
                self.velocity[1] -= 10
                jump_sfx = pygame.mixer.Sound("Sounds/Jump.wav")
                jump_sfx.set_volume(self.volume)
                if self.volume > 0.04:
                    jump_sfx.play()

        if keys[pygame.K_ESCAPE]:
            self.is_paused = True


    def is_on_ground(self):
        for tile in self.tile_list:
            if tile.rect.colliderect(self.rect.x, self.rect.y + self.velocity[1], self.rect.width, self.rect.height):
                if self.velocity[1] >= 0:
                    return True
    
        return False