import pygame

class Button:
    def __init__(self, image, image2, width, height, x, y):
        self.image = image
        self.image = pygame.transform.scale(self.image, (width, height))
        self.rect = self.image.get_rect()
        self.image2 = image2
        self.image2 = pygame.transform.scale(self.image2, (width, height))
        self.rect = self.image2.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.hover = False
        self.clicked = False

    def draw(self, screen):
        action = False

        mousePos = pygame.mouse.get_pos()

        if self.rect.collidepoint(mousePos):
            screen.blit(self.image2, self.rect)
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                action = True
                self.clicked = True
        else:
            screen.blit(self.image, self.rect)

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        return action
        action = False
    
class Title():
    def __init__(self, image, width, height, x, y):
        self.image = image
        self.image = pygame.transform.scale(self.image, (width, height))
        self.rect = self.image.get_rect()            
        self.rect.x = x
        self.rect.y = y

    def draw(self, screen):
        screen.blit(self.image, self.rect)