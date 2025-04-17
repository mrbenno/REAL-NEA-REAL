# imports:
import pygame
from Character import Enemy  # import Enemy class so enemies can be spawned into the world


# Tile class stores info about each tile's position, type, and colour
class Tile:
    def __init__(self, rect, kind, colour):
        self.rect = rect          # pygame.Rect object for collision and drawing
        self.kind = kind          # tile type (1 = normal, 2 = hazard, 4 = goal)
        self.colour = colour      # visual colour of the tile


# World class manages building and drawing the level from 2D grid data
class World:
    def __init__(self, data):
        self.data = data  # 2D array of tile values
        # colours for different tile types
        self.colour = "#2E4D4C"        # standard ground tile
        self.danger_colour = "#DC2F02" # lava/hazard tile
        self.end_colour = "#007EF5"    # goal tile
        self.tile_list = []            # stores all created tiles

    def build_world(self, tile_size, sprite_group):
        row_count = 0  # keeps track of the current row
        tile = 0       # dummy var to return at the end (not actually used?)

        for row in self.data:
            column_count = 0  # keeps track of the current column in the row
            for tile in row:
                # tile == 1: solid tile
                if tile == 1:
                    tile = pygame.Rect((tile_size * column_count, tile_size * row_count), (tile_size, tile_size))
                    self.tile_list.append(Tile(tile, 1, self.colour))

                # tile == 2: hazard/lava tile
                elif tile == 2:
                    tile = pygame.Rect((tile_size * column_count, tile_size * row_count), (tile_size, tile_size))
                    self.tile_list.append(Tile(tile, 2, self.danger_colour))

                # tile == 3: enemy spawn (uses Enemy class)
                elif tile == 3:
                    spike = Enemy(tile_size * column_count, tile_size * row_count)
                    sprite_group.add(spike)

                # tile == 4: goal/end tile
                elif tile == 4:
                    tile = pygame.Rect((tile_size * column_count, tile_size * row_count), (tile_size, tile_size))
                    self.tile_list.append(Tile(tile, 4, self.end_colour))

                column_count += 1  # move to next column
            row_count += 1  # move to next row

        return self.tile_list, tile  # returns all created tiles and final dummy 'tile'

    def draw(self, screen):
        # draw each tile as a coloured rectangle
        for tile in self.tile_list:
            pygame.draw.rect(screen, tile.colour, tile.rect)