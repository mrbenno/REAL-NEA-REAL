import pygame

# button class used for menus and quizzes
class Button:
    def __init__(self, image, image2, width, height, x, y):
        # default and hover image setup
        self.image = image
        self.image = pygame.transform.scale(self.image, (width, height))

        self.image2 = image2
        self.image2 = pygame.transform.scale(self.image2, (width, height))

        # set position and size
        self.rect = self.image2.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.hover = False
        self.clicked = False

    def draw(self, screen):
        action = False
        mouse_pos = pygame.mouse.get_pos()

        # check for hover and click
        if self.rect.collidepoint(mouse_pos):
            screen.blit(self.image2, self.rect)
            if pygame.mouse.get_pressed()[0] == 1 and not self.clicked:
                action = True
                self.clicked = True
        else:
            screen.blit(self.image, self.rect)

        # reset click state
        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        return action

# title class for menus or screens
class Title:
    def __init__(self, image, width, height, x, y):
        self.image = image
        self.image = pygame.transform.scale(self.image, (width, height))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def draw(self, screen):
        screen.blit(self.image, self.rect)
        return True

# quiz class handles question logic and options
class Quiz:
    def __init__(self, question, width, height, choices, correct_answer):
        # scale question image
        self.question = question
        self.question = pygame.transform.scale(self.question, (width, height))
        self.rect = self.question.get_rect()
        self.rect.x = 50
        self.rect.y = 25

        # where to place each answer
        self.coords = [(110, 340), (410, 340), (110, 440), (410, 440)]

        # render text answers
        self.font = pygame.font.Font("Fonts/Pixeltype.ttf", 50)
        self.rendered_choices = []
        for choice in choices:
            self.rendered_choices.append(self.font.render(choice, True, '#ffffff'))

        self.correct_answer = correct_answer
        self.incorrect_counter = 0

        # load all icon images for option buttons
        self.options_icons = []
        for i in range(1, 9):
            self.options_icons.append(pygame.image.load(f"Assets/Options/Options-{i}.png"))

        # create four answer buttons
        self.option_1 = Button(self.options_icons[0], self.options_icons[1], 50, 50, 50, 340)
        self.option_2 = Button(self.options_icons[2], self.options_icons[3], 50, 50, 350, 340)
        self.option_3 = Button(self.options_icons[4], self.options_icons[5], 50, 50, 50, 440)
        self.option_4 = Button(self.options_icons[6], self.options_icons[7], 50, 50, 350, 440)

        # load result images for feedback
        self.correct_label = pygame.image.load("Assets/Result-1.png")
        self.correct = Title(self.correct_label, 570, 160, 360 - 285, 200)

        self.incorrect_label = pygame.image.load("Assets/Result-2.png")
        self.incorrect = Title(self.incorrect_label, 670, 160, 360 - 335, 200)

    def draw(self, screen):
        # draw question and answers
        screen.blit(self.question, self.rect)
        for i in range(4):
            screen.blit(self.rendered_choices[i], self.coords[i])

        # return answer choice when clicked
        if self.option_1.draw(screen):
            return 1
        elif self.option_2.draw(screen):
            return 2
        elif self.option_3.draw(screen):
            return 3
        elif self.option_4.draw(screen):
            return 4

    def check_answer(self, draw, screen):
        # check if selected answer is correct
        if draw == self.correct_answer:
            return True
        else:
            self.incorrect_counter += 1
            return False
