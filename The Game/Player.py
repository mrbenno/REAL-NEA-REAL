import pygame

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

    # function which animates player
    def animate(self, x, y):
        self.velocity[0] += x
        self.velocity[1] += y
        # friendly reminder #1: self means actual object being edited, anything not 'self.' normal var
    
    def draw(self, screen):
        pygame.draw.rect(screen, (self.colour), self.rect)

    #GPT-assisted code, works as expected, although improvements may be made.
    def update(self, tileList):

        self.velocity[1] += 0.5
        for i in range(10):
            self.checkCollisions(tileList)

        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]

        self.velocity[0] *= 0.1
        self.velocity[1] *= 0.98

    #self.rect.move_by(...)

    def checkInput(self):
        keys = pygame.key.get_pressed()
        
        #left and right always active, no restraints
        if keys[pygame.K_a]: #moving left   
            self.animate(-self.speed, 0)    
        if keys[pygame.K_d]: #moving right
            self.animate(self.speed, 0)
        
        if self.isJumping == False: #must be here otherwise would jump infinitly
            if keys[pygame.K_SPACE]: # jumping
                self.isJumping = True
        else:
            if self.jumpCount >= -8: #opposite of what was previosuly set,makes for euqal jump
                negative = 1 #if this value is one, the player will fall down
                if self.jumpCount < 0: #top of the jump
                    negative = -1 #player will fall down
                jumpSize = (self.jumpCount ** 2) * 0.25 * negative
                self.rect.y -= jumpSize #changing the player's y position
                # newScale -= (self.jumpCount ** 2) * 0.025 * negative #changing the player's shape
                # self.rect.x -= (self.rect.width - newScale) * 0.5
                # self.rect.width   -= (self.jumpCount ** 2) * 0.025 * negative
                # self.rect.height  += (self.jumpCount ** 2) * 0.025 * negative
                self.jumpCount -= 0.5 
            else:
                self.isJumping = False
                self.jumpCount = 8

    def checkCollisions(self, tileList):

        for tile in tileList:         
            if tile.colliderect(self.rect.x + self.velocity[0], self.rect.y, self.rect.width, self.rect.height):
                self.velocity[0] = 0

            if tile.colliderect(self.rect.x, self.rect.y + self.velocity[1], self.rect.width, self.rect.height):
                ##jumping upwards / ground below
                if self.velocity[1] < 0:
                    self.rect.top = tile.bottom
                    self.velocity[1] = 0
	            #falling down / ground above
                elif self.velocity[1] >= 0:
                    self.rect.bottom = tile.top
                    self.velocity[1] = 0 