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
    def __init__(self, data):
        self.data = data
        self.colour = "#2E4D4C"
        self.danger_colour = "#DC2F02"
        self.end_colour = "#007EF5"
        self.tile_list = []

    def build_world(self, tile_size, sprite_group):
        row_count = 0
        tile = 0
        for row in self.data:
            column_count = 0
            for tile in row:
                if tile == 1:
                    tile = pygame.Rect((tile_size * column_count, tile_size * row_count), (tile_size, tile_size))
                    self.tile_list.append(Tile(tile, 1, self.colour))
                elif tile == 2:
                    tile = pygame.Rect((tile_size * column_count, tile_size * row_count), (tile_size, tile_size))
                    self.tile_list.append(Tile(tile, 2, self.danger_colour))
                elif tile == 3:
                    # spike is an instance of the Enemy class, x and y are the positions of the tile
                    spike = Enemy(tile_size * column_count, tile_size * row_count)
                    sprite_group.add(spike)
                elif tile == 4:
                    tile = pygame.Rect((tile_size * column_count, tile_size * row_count), (tile_size, tile_size))
                    self.tile_list.append(Tile(tile, 4, self.end_colour))
                column_count += 1
            row_count += 1
        return self.tile_list, tile
    

    def draw(self, screen):
        for tile in self.tile_list:
            pygame.draw.rect(screen, tile.colour, tile.rect)