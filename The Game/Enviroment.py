# imports:
import pygame
from Character import Enemy


# creating the class Tile, makes program more efficient later
class Tile:
    def __init__(self, rect, kind, colour):
        self.rect = rect
        self.kind = kind
        self.colour = colour


# the world class is created,
class World:
    def __init__(self, data, colour):
        self.data = data
        self.colour = colour
        self.dangerColour = "#DC2F02"
        self.tileList = []

    def build_world(self, tile_size, sprite_group):
        row_count = 0
        tile = 0
        for row in self.data:
            column_count = 0
            for tile in row:
                if tile == 1:
                    tile = pygame.Rect((tile_size * column_count, tile_size * row_count), (tile_size, tile_size))
                    self.tileList.append(Tile(tile, 1, self.colour))
                elif tile == 2:
                    tile = pygame.Rect((tile_size * column_count, tile_size * row_count), (tile_size, tile_size))
                    self.tileList.append(Tile(tile, 2, self.dangerColour))
                elif tile == 3:
                    # spike is an instance of the Enemy class, x and y are the positions of the tile
                    spike = Enemy(tile_size * column_count, tile_size * row_count)
                    sprite_group.add(spike)
                column_count += 1
            row_count += 1
        return self.tileList, tile

    def draw(self, screen):
        for tile in self.tileList:
            pygame.draw.rect(screen, tile.colour, tile.rect)