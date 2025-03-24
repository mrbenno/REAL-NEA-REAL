import pygame

pygame.init()
pygame.joystick.init()

class Player:
    #constructer
    def __init__(self, rect, colour, speed, isJumping, onGround, jumpCount):
        self.rect = rect
        self.colour = colour
        self.velocity = [0, 0]
        self.speed = speed
        self.isJumping = isJumping
        self.onGround = onGround
        self.jumpCount = jumpCount
        self.tileList = []
        self.isDead = False

    def updateTileList(self, new):
        self.tileList = new

    # function which animates player
    def animate(self, x, y):
        self.velocity[0] += x
        self.velocity[1] += y
        # friendly reminder #1: self means actual object being edited, anything not 'self.' normal var
    
    def draw(self, screen):
        pygame.draw.rect(screen, (self.colour), self.rect)

    def update(self):
        for i in range(1):
            self.checkCollisions()

        self.velocity[1] += 0.6
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]

        self.velocity[0] *= 0.1
        self.velocity[1] += 0.0

    def checkIfDead(self, height):
        if self.rect.y > height:
            self.rect.x, self.rect.y = 100, 100
            deathSFX = pygame.mixer.Sound("Sounds/Death.wav")
            deathSFX.play()

    #self.rect.move_by(...)

    def checkInput(self):
        keys = pygame.key.get_pressed()
        
        #left and right always active, no restraints
        if keys[pygame.K_a]: #moving left   
            self.velocity[0] = -10
        if keys[pygame.K_d]: #moving right
            self.velocity[0] = 10
        
        if keys[pygame.K_SPACE] and self.isOnGround():
            jumpSFX = pygame.mixer.Sound("Sounds/Jump.wav")
            jumpSFX.play()
            self.velocity[1] -= 10


    def checkCollisions(self):
        for tile in self.tileList:         
            if tile.colliderect(self.rect.x + self.velocity[0], self.rect.y + self.rect.height / 4, self.rect.width / 2, self.rect.height / 2):
                self.velocity[0] += 10
            elif tile.colliderect(self.rect.x + self.velocity[0] + self.rect.width / 2, self.rect.y+ self.rect.height / 4, self.rect.width / 2, self.rect.height / 2):
                self.velocity[0] -= 10
            if tile.colliderect(self.rect.x, self.rect.y + self.velocity[1], self.rect.width, self.rect.height):
                ##jumping upwards / ground below (in pygame speak)
                if self.velocity[1] < 0:
                    self.rect.top = (tile.bottom + 0.1)
                    self.velocity[1] = 0
            #falling down / ground above
                elif self.velocity[1] >= 0:
                    self.rect.bottom = (tile.top - 0.1)
                    self.velocity[1] = 0 

    def isOnGround(self):
        for tile in self.tileList:
            if tile.colliderect(self.rect.x, self.rect.y + self.velocity[1], self.rect.width, self.rect.height):
                if self.velocity[1] >= 0:
                    return True
        return False