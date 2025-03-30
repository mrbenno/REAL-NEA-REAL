import pygame
import time
import random
import math
 
from Character import Player, Enemy
from Enviroment import World, Button

def main():
    pygame.init()

    screen = pygame.display.set_mode((720, 540))
    dimensions = [screen.get_width(), screen.get_height()]
    frame = pygame.time.Clock()

    tileSize = 30

    data3 = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 3, 0, 0, 0, 0, 0],
    [1, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 1, 1, 1, 1, 2, 2, 2, 1, 1, 1],
    ]

    #load images
    pause = pygame.image.load("Assets/PauseBtn.PNG")
    paused = pygame.image.load("Assets/pauseBtnDown.PNG")

    player1 = Player(pygame.Rect(60, dimensions[1] - 60, 25, 25), '#0A9B9A', 5, False, False, 8)
    spikeGroup = pygame.sprite.Group()
    world3 = World(data3, '#2E4D4C')
    world3.buildWorld(tileSize, spikeGroup)
    pauseButton = Button(pause, paused, 30, 30, dimensions[0] - 45, 45)

    while True:
        handleEvents()  

        player1.updateTileList(world3.tileList)

        if not player1.isPaused:
            player1.checkInput()
            player1.update()

        drawEverything(screen, world3, player1, spikeGroup, pauseButton)

        if pauseButton.draw == True:
            player1.isPaused = True

        if player1.checkIfDead(540, spikeGroup):
            deathSFX = pygame.mixer.Sound("Sounds/Death.wav")
            deathSFX.play()
            player1.rect.x, player1.rect.y = player1.spawnPoint
            player1.velocity = [0,0]

        pygame.display.flip() #display.flip updates entire screen, diaplay.update updates what's in brackets 
        frame.tick(60)

    return newScale

def handleEvents():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

def drawEverything(screen, world, player, enemies, pause):
    screen.fill('#0A141F')

    world.draw(screen)
    player.draw(screen)
    enemies.draw(screen)
    pause.draw(screen)



main()