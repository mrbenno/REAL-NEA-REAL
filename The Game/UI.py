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

        mouse_pos = pygame.mouse.get_pos()

        if self.rect.collidepoint(mouse_pos):
            screen.blit(self.image2, self.rect)
            if pygame.mouse.get_pressed()[0] == 1 and not self.clicked:
                action = True
                self.clicked = True
        else:
            screen.blit(self.image, self.rect)

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        return action
        # action = False


class Title:
    def __init__(self, image, width, height, x, y):
        self.image = image
        self.image = pygame.transform.scale(self.image, (width, height))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def draw(self, screen):
        screen.blit(self.image, self.rect)

class Menu():
    def __init__(self, bg_colour, player, title, button1, button2, button3):
        self.player = player
        self.title = title
        self.button1 = button1
        self.button2 = button2
        self.button3 = button3

    def draw(self, screen):
        screen.fill('#000000')
        self.title.draw(screen)

        if self.button1.draw(screen):
            return 1

        if self.button2.draw(screen):
            return 2

        if self.button3 is not None:
            if self.button3.draw(screen):
                return 3
            

class Paragraph():
    def __init__(self, paragraph, font_size, font, x, y, leading):
        self.paragraph = paragraph
        self.font_size = font_size
        self.font = font
        self.x = x
        self.y = y
        self.leading = leading


    def render_list(self):
        rendered = [] # creates list to store rendered text in
        for i, line in enumerate(self.paragraph.split('\n')): # for i in line breaks (\n)
            text_surface, text_rect = self.font.render(line, '#FFFFFF') # assigns the text_surface and text_rect variables to Pygame's text rendering function
            text_rect.topleft = (self.x, self.y + i, * (self.font_size + self.leading)) # top left co-ord of the rect is assigned to these values so that it can change with each new line
            rendered.append(text_surface, text_rect) # surface and rect are added to the list as tuples

            return text_surface, text_rect, rendered
     
        
    def draw(self, screen, rendered):
        screen.fill('#000000')
        for text_surface, text_rect in rendered:
            screen.blit(text_surface, text_rect)
        return True


