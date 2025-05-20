import pygame
import random # Import the random module

class Enemy:
    def __init__(self, x, y, smiley, health, color):
        self.x = x  # Grid coordinate
        self.y = y  # Grid coordinate
        self.smiley = smiley
        self.max_health = health
        self.health = health
        self.color = color
        self.is_dead = False
        self.vision_radius = 5 # Range in tiles enemy can see the player
        self.attack_power = 5 # Enemy attack power

    def move(self, target_x, target_y, game_map, player): # Add player object
        if self.is_dead:
            return

        # Calculate distance to player
        distance_x = target_x - self.x
        distance_y = target_y - self.y
        distance = (distance_x**2 + distance_y**2)**0.5

        dx, dy = 0, 0 # Intended move direction

        if distance < self.vision_radius:
            # Determine movement direction towards player
            if distance_x > 0: dx = 1
            elif distance_x < 0: dx = -1
            
            if distance_y > 0: dy = 1
            elif distance_y < 0: dy = -1
        else:
            # Random movement if player is not in vision
            dx = random.choice([-1, 0, 1])
            dy = random.choice([-1, 0, 1])
            if dx == 0 and dy == 0: # Don't stand still if choosing random move
                return 

        # Calculate potential new position
        next_x, next_y = self.x + dx, self.y + dy

        # Check if the target tile is the player
        if next_x == player.x and next_y == player.y:
            print(f"Enemy {self.smiley} attacks player!")
            player.take_damage(self.attack_power)
            return # Enemy attacks instead of moving

        # Attempt to move (if not attacking player)
        # This simplified logic tries the determined dx, dy.
        # A more complex version would try alternatives if the primary path is blocked.
        if (dx != 0 or dy != 0): # Only attempt move if there's a direction
            # Check if trying to move diagonally
            if dx != 0 and dy != 0:
                if game_map.is_walkable(next_x, next_y):
                    self.x = next_x
                    self.y = next_y
                    return
                # Fallback: try horizontal then vertical if diagonal is blocked
                if game_map.is_walkable(self.x + dx, self.y):
                    self.x += dx
                    return
                if game_map.is_walkable(self.x, self.y + dy):
                    self.y += dy
                    return
            # Horizontal move
            elif dx != 0:
                if game_map.is_walkable(next_x, self.y):
                    self.x = next_x
                    return
            # Vertical move
            elif dy != 0:
                if game_map.is_walkable(self.x, next_y):
                    self.y = next_y
                    return
        
        # If player was in vision but path was blocked, or random move was blocked, try a purely random valid move
        # This is a fallback to prevent enemies from getting stuck too easily if their target is blocked.
        if distance < self.vision_radius: # Only do this extra random move if player was initially in vision.
            random_dx = random.choice([-1, 0, 1])
            random_dy = random.choice([-1, 0, 1])
            if not (random_dx == 0 and random_dy == 0):
                 if game_map.is_walkable(self.x + random_dx, self.y + random_dy):
                    # Check again to ensure it's not the player tile for this random fallback
                    if not (self.x + random_dx == player.x and self.y + random_dy == player.y):
                        self.x += random_dx
                        self.y += random_dy

    def draw(self, screen, font, tile_size):
        if not self.is_dead:
            text_surface = font.render(self.smiley, True, self.color)
            # Convert grid coordinates to pixel coordinates for drawing
            pixel_x = self.x * tile_size
            pixel_y = self.y * tile_size
            screen.blit(text_surface, (pixel_x, pixel_y))

    def take_damage(self, damage):
        if not self.is_dead:
            self.health -= damage
            if self.health <= 0:
                self.health = 0
                self.is_dead = True
                print(f"Enemy {self.smiley} at ({self.x}, {self.y}) has died.")
                # In a more complex game, this might trigger an animation or drop loot
                # For now, it just sets the flag and prints a message.
                # The actual removal from the game's enemy list will be handled in main.py
