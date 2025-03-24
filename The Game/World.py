import pygame

class World():
    def __init__(self, data, colour):
        self.data = data
        self.colour = colour
        self.tileList = []

    def buildWorld(self, tileSize):
        rowCount = 0
        for row in self.data:
            coloumnCount = 0
            for tile in row:
                if tile == 1:
                    tile = pygame.Rect((tileSize * coloumnCount, tileSize * rowCount), (tileSize, tileSize))
                    self.tileList.append(tile)
                coloumnCount += 1
            rowCount += 1
        return self.tileList, tile
    
    def draw(self, screen):
        for tile in self.tileList:
            pygame.draw.rect(screen, self.colour, tile)