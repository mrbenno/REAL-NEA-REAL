import pygame

pygame.init()

class Player:
    def __init__(self, rect, colour, speed, isJumping, onGround, jumpCount):       
        self.rect = rect
        self.spawnPoint = (self.rect.x, self.rect.y) 
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

    def checkIfDead(self, height):
        if self.rect.y > height:
            return True
        for tile in self.tileList:         
            if tile.rect.colliderect(self.rect.x, self.rect.y + self.velocity[1], self.rect.width, self.rect.height):
                if tile.kind == 2:
                    return True
                
    def update(self):
        print(self.velocity)
        for i in range(1):
            self.checkCollisions()

        self.velocity[1] += 0.6
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]

        self.velocity[0] *= 0.1
        self.velocity[1] += 0.0

        if self.checkIfDead(540):
            deathSFX = pygame.mixer.Sound("Sounds/Death.wav")
            deathSFX.play()
            self.rect.x, self.rect.y = self.spawnPoint
            self.velocity = [0,0]


                
    #self.rect.move_by(...)

    def checkInput(self):
        keys = pygame.key.get_pressed()
        
        #left and right always active, no restraints
        if keys[pygame.K_a]: #moving left   
            self.velocity[0] = -10
        if keys[pygame.K_d]: #moving right
            self.velocity[0] = 10
        
        if (keys[pygame.K_SPACE] or keys[pygame.K_SPACE]) and self.isOnGround():
            self.velocity[1] -= 10
            jumpSFX = pygame.mixer.Sound("Sounds/Jump.wav")
            jumpSFX.play()


    def checkCollisions(self):
        for tile in self.tileList:         
            if tile.rect.colliderect(self.rect.x + self.velocity[0], self.rect.y + self.rect.height / 4, self.rect.width / 2, self.rect.height / 2):
                self.velocity[0] += 10
            elif tile.rect.colliderect(self.rect.x + self.velocity[0] + self.rect.width / 2, self.rect.y+ self.rect.height / 4, self.rect.width / 2, self.rect.height / 2):
                self.velocity[0] -= 10
            if tile.rect.colliderect(self.rect.x, self.rect.y + self.velocity[1], self.rect.width, self.rect.height):
                ##jumping upwards / ground below (in pygame speak)
                if self.velocity[1] < 0:
                    self.rect.top = (tile.rect.bottom + 0.1)
                    self.velocity[1] = 0
            #falling down / ground above
                elif self.velocity[1] >= 0:
                    self.rect.bottom = (tile.rect.top - 0.1)
                    self.velocity[1] = 0 

    def isOnGround(self):
        for tile in self.tileList:
            if tile.rect.colliderect(self.rect.x, self.rect.y + self.velocity[1], self.rect.width, self.rect.height):
                if self.velocity[1] >= 0:
                    return True
        return False
    
class Enemy:
    pass
