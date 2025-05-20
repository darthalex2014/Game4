import pygame

# Define colors for map elements
WALL_COLOR = (100, 100, 100)
FLOOR_COLOR = (50, 50, 50)

class Map:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.tiles = self._create_basic_map()

    def _create_basic_map(self):
        new_tiles = [['.' for _ in range(self.width)] for _ in range(self.height)]
        # Create walls around the border
        for y in range(self.height):
            for x in range(self.width):
                if x == 0 or x == self.width - 1 or \
                   y == 0 or y == self.height - 1:
                    new_tiles[y][x] = '#'
        return new_tiles

    def draw(self, screen, font, tile_size):
        for y in range(self.height):
            for x in range(self.width):
                char_to_render = self.tiles[y][x]
                color = WALL_COLOR if char_to_render == '#' else FLOOR_COLOR
                
                # Optimization: Don't render floor tiles if they are just dots,
                # let the background color show through if it's the same.
                # However, for this exercise, we'll render them explicitly.
                text_surface = font.render(char_to_render, True, color)
                screen.blit(text_surface, (x * tile_size, y * tile_size))

    def is_walkable(self, x, y):
        # Check if the coordinates are within map boundaries
        if not (0 <= x < self.width and 0 <= y < self.height):
            return False
        # Check if the tile is a floor tile
        if self.tiles[y][x] == '.':
            return True
        return False
