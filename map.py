import pygame
import random
from items import Food # Import Food class

# Define colors for map elements
WALL_COLOR = (100, 100, 100)
FLOOR_COLOR = (50, 50, 50)
FOOD_COLOR = (0, 255, 0) # Green for food items like apples

# --- Rect Class (for room geometry) ---
class Rect:
    def __init__(self, x, y, w, h):
        self.x1 = x
        self.y1 = y
        self.x2 = x + w
        self.y2 = y + h

    def center(self):
        center_x = (self.x1 + self.x2) // 2
        center_y = (self.y1 + self.y2) // 2
        return (center_x, center_y)

    def intersects(self, other):
        # Returns true if this rectangle intersects with another one
        return (self.x1 <= other.x2 and self.x2 >= other.x1 and
                self.y1 <= other.y2 and self.y2 >= other.y1)

# --- Map Class ---
class Map:
    def __init__(self, width, height): # player_start_x, player_start_y removed
        self.width = width
        self.height = height
        self.rooms = []
        self.items = []
        
        # Dungeon generation parameters
        self.max_rooms = 10
        self.room_min_size = 6
        self.room_max_size = 10
        
        # Player start position, to be determined by dungeon generation
        self.player_start_x = 0 
        self.player_start_y = 0

        self._generate_dungeon()

    def _generate_dungeon(self):
        # 1. Initialize all tiles to walls
        self.tiles = [['#' for _ in range(self.width)] for _ in range(self.height)]
        self.rooms = [] # Clear rooms for regeneration
        self.items = [] # Clear items for regeneration

        # 2. Room Generation
        for _ in range(self.max_rooms):
            w = random.randint(self.room_min_size, self.room_max_size)
            h = random.randint(self.room_min_size, self.room_max_size)
            # Position must be within map boundaries, ensuring room fits
            x = random.randint(1, self.width - w - 1) # -1 to keep a border wall
            y = random.randint(1, self.height - h - 1) # -1 to keep a border wall

            new_room = Rect(x, y, w, h)
            
            # Check for intersections with existing rooms
            failed = False
            for other_room in self.rooms:
                if new_room.intersects(other_room):
                    failed = True
                    break
            
            if not failed:
                # "Carve" out the room
                self._create_room(new_room)
                self.rooms.append(new_room)

        # 3. Corridor Generation (if rooms exist)
        if self.rooms:
            for i in range(1, len(self.rooms)):
                prev_center_x, prev_center_y = self.rooms[i-1].center()
                new_center_x, new_center_y = self.rooms[i].center()

                if random.randint(0, 1) == 0:
                    self._create_h_tunnel(prev_center_x, new_center_x, prev_center_y)
                    self._create_v_tunnel(prev_center_y, new_center_y, new_center_x)
                else:
                    self._create_v_tunnel(prev_center_y, new_center_y, prev_center_x)
                    self._create_h_tunnel(prev_center_x, new_center_x, new_center_y)
        
        # 4. Player Starting Position
        if self.rooms:
            self.player_start_x, self.player_start_y = self.rooms[0].center()
        else:
            # Fallback if no rooms generated (shouldn't happen with reasonable params)
            self.player_start_x = self.width // 2
            self.player_start_y = self.height // 2
            # Ensure this fallback is walkable by carving a small area
            self.tiles[self.player_start_y][self.player_start_x] = '.'


        # 5. Item Placement
        self._place_items() # No longer needs player_start_x, player_start_y as args

    def _create_room(self, room):
        # Carve a room, ensuring x1 < x2 and y1 < y2
        for x in range(room.x1, room.x2):
            for y in range(room.y1, room.y2):
                # Check bounds just in case, though room placement should handle this
                if 0 < x < self.width -1 and 0 < y < self.height -1:
                    self.tiles[y][x] = '.'
    
    def _create_h_tunnel(self, x1, x2, y):
        for x in range(min(x1, x2), max(x1, x2) + 1):
            if 0 < x < self.width -1 and 0 < y < self.height -1: # Boundary checks
                self.tiles[y][x] = '.'

    def _create_v_tunnel(self, y1, y2, x):
        for y in range(min(y1, y2), max(y1, y2) + 1):
             if 0 < x < self.width -1 and 0 < y < self.height -1: # Boundary checks
                self.tiles[y][x] = '.'

    def _place_items(self): # player_start_x, player_start_y removed from args
        if not self.rooms: # Don't place items if there are no rooms
            return

        num_food_items = 3 
        placed_item_locations = set()

        for _ in range(num_food_items):
            placed = False
            for _ in range(100): # Try 100 times to place an item
                # Pick a random room
                room = random.choice(self.rooms)
                # Pick a random tile within the room (excluding room borders)
                item_x = random.randint(room.x1, room.x2 -1) 
                item_y = random.randint(room.y1, room.y2 -1)

                if self.tiles[item_y][item_x] == '.' and \
                   (item_x != self.player_start_x or item_y != self.player_start_y) and \
                   (item_x, item_y) not in placed_item_locations:
                    
                    self.items.append(Food(item_x, item_y, '%', "Apple", FOOD_COLOR, 20))
                    placed_item_locations.add((item_x, item_y))
                    placed = True
                    break
            if not placed:
                print("Warning: Could not place all food items.")


    def draw(self, screen, font, tile_size):
        # Draw terrain tiles
        for y in range(self.height):
            for x in range(self.width):
                char_to_render = self.tiles[y][x]
                color = WALL_COLOR if char_to_render == '#' else FLOOR_COLOR
                
                text_surface = font.render(char_to_render, True, color)
                screen.blit(text_surface, (x * tile_size, y * tile_size))
        
        # Draw items on top
        for item in self.items:
            item.draw(screen, font, tile_size)

    def is_walkable(self, x, y):
        # Check if the coordinates are within map boundaries
        if not (0 <= x < self.width and 0 <= y < self.height):
            return False
        # Check if the tile is a floor tile
        if self.tiles[y][x] == '.':
            return True
        return False
