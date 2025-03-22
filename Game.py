import pygame
from pygame.locals import * # imports eerything from namespace into this program, supposidly stops me typing as much
from World import World
from Player import Player

pygame.init()

screenWidth = 100
screenHeight = 100
screen = pygame.display.set_mode((screenWidth, screenHeight))
frame = pygame.time.Clock()

tileSize = 10

World.data = [
[1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]

def handleEvents():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

def main():
    while True:
        handleEvents()
        pygame.display.update() #display.flip updates entire screen, diaplay.update updates what's in brackets
        frame.tick(60)

main()