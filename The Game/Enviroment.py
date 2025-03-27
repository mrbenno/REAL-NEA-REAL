import pygame

class Tile():
    def __init__(self, rect, kind, colour):
        self.rect = rect
        self.kind = kind
        self.colour = colour

class World():
    def __init__(self, data, colour):
        self.data = data
        self.colour = colour
        self.dangerColour = "#DC2F02"
        self.tileList = []

    def buildWorld(self, tileSize):
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
                coloumnCount += 1
            rowCount += 1
        return self.tileList, tile

    def draw(self, screen):
        for tile in self.tileList:
            pygame.draw.rect(screen, tile.colour, tile.rect)

class Button:
    pass