import pygame

class Item:
    def __init__(self, x, y, smiley, name, color):
        self.x = x  # Grid coordinate
        self.y = y  # Grid coordinate
        self.smiley = smiley
        self.name = name
        self.color = color

    def draw(self, screen, font, tile_size):
        text_surface = font.render(self.smiley, True, self.color)
        # Convert grid coordinates to pixel coordinates for drawing
        pixel_x = self.x * tile_size
        pixel_y = self.y * tile_size
        screen.blit(text_surface, (pixel_x, pixel_y))

class Food(Item):
    def __init__(self, x, y, smiley, name, color, hunger_value):
        super().__init__(x, y, smiley, name, color)
        self.hunger_value = hunger_value
