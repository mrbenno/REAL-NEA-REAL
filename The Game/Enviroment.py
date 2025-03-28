#imports
import pygame
from Character import Enemy

# creating the class Tile, makes program more efficient later 
class Tile():
    def __init__(self, rect, kind, colour):
        self.rect = rect
        self.kind = kind
        self.colour = colour

#the world class is created, 
class World():
    def __init__(self, data, colour):
        self.data = data
        self.colour = colour
        self.dangerColour = "#DC2F02"
        self.tileList = []

    def buildWorld(self, tileSize, spriteGroup):
        rowCount = 0
        for row in self.data:
            coloumnCount = 0
            for tile in row:
                if tile == 1:
                    tile = pygame.Rect((tileSize * coloumnCount, tileSize * rowCount), (tileSize, tileSize))
                    self.tileList.append(Tile(tile, 1, self.colour))
                elif tile == 2:
                    tile = pygame.Rect((tileSize * coloumnCount, tileSize * rowCount), (tileSize, tileSize))
                    self.tileList.append(Tile(tile, 2, self.dangerColour))
                elif tile == 3:
                    spike = Enemy(tileSize * coloumnCount, tileSize * rowCount) #spike is an instance of the Enemy class, x and y are the positions of the tile
                    spriteGroup.add(spike)
                coloumnCount += 1
            rowCount += 1
        return self.tileList, tile

    def draw(self, screen):
        for tile in self.tileList:
            pygame.draw.rect(screen, tile.colour, tile.rect)

class Button:
    pass