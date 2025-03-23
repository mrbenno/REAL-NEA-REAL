import pygame

class Player:
    #constructer
    def __init__(self, rect, colour, speed, deltaX, deltaY, isJumping, onGround, jumpCount):
        self.rect = rect
        self.colour = colour
        self.velocity = [0, 0]
        self.deltaX = 1
        self.deltaY = 1
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
        deltaX = self.velocity[0]
        deltaY = self.velocity[1]

        self.checkCollisions(tileList, deltaY, deltaX)

        self.rect.x += deltaX
        self.rect.y += deltaY

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

    def checkCollisions(self, tileList, deltaX, deltaY):
        self.onGround = False

        for tile in tileList:         
            if pygame.Rect.colliderect(tile, self.rect):
                print("collided")            
                #checks if below ground/jumping
                if self.velocity[1] < 0:
                    deltaY = tile.bottom - self.rect.top
                    self.velocity[1] = 0
                    self.animate(0, deltaY)

                    #checks if above ground/falling
                if self.velocity[1] >= 0:
                    deltaY = tile.top - self.rect.bottom
                    self.velocity[1] = 0
                    self.animate(0, deltaY) 

        #     if pygame.Rect.colliderect(tile, self.rect):
        #         print("collided")

        #         if deltaX < 0: #moving left
        #             self.rect.left = tile.right
        #             self.velocity[0] = 0

        #         if deltaX > 0: #moving right
        #             self.rect.right = tile.left
        #             self.velocity[0] = 0

        #         if deltaY < 0: #jumping upwards / platform above
        #             self.rect.top = tile.bottom
        #             self.velocity[1] = 0
        #         elif deltaY > 0: #falling down / ground below
        #             self.rect.bottom # tile.top
        #             self.velocity[1] = 0
        #             self.onGround = True      

        # if not self.onGround == True:
        #     self.velocity[1] += 0.05
