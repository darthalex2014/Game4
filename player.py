import pygame

# Define colors (though WHITE is often defined in main, it's good practice if Player is self-contained)
WHITE = (255, 255, 255)

class Player:
    def __init__(self, x, y, smiley):
        self.x = x  # Grid coordinate
        self.y = y  # Grid coordinate
        self.smiley = smiley
        self.color = WHITE

        self.max_health = 100
        self.health = self.max_health

        self.max_hunger = 100
        self.hunger = self.max_hunger
        self.is_dead = False # Initialize is_dead flag

    def update_hunger(self):
        self.hunger -= 1
        if self.hunger < 0:
            self.hunger = 0
        
        if self.hunger == 0:
            # Apply penalty for starvation
            self.health -= 1 # Direct modification for now
            if self.health < 0:
                self.health = 0
                # Potentially handle player death here or in the game loop

    def eat(self, food_value):
        self.hunger += food_value
        if self.hunger > self.max_hunger:
            self.hunger = self.max_hunger

    def take_damage(self, damage):
        self.health -= damage
        if self.health <= 0:
            self.health = 0
            self.is_dead = True # Set is_dead flag
            print("Player has died!") # Keep the print for console feedback

    def move(self, dx, dy, game_map, enemies): # Add enemies list
        new_x = self.x + dx
        new_y = self.y + dy
        attack_power = 10

        # Check for enemy at the target location
        for enemy in enemies:
            if not enemy.is_dead and enemy.x == new_x and enemy.y == new_y:
                print(f"Player attacks enemy {enemy.smiley} at ({enemy.x}, {enemy.y})")
                enemy.take_damage(attack_power)
                self.update_hunger() # Attacking also costs hunger
                return # Player attacks instead of moving

        # If no enemy, proceed with normal movement
        if game_map.is_walkable(new_x, new_y):
            self.x = new_x
            self.y = new_y
            self.update_hunger() # Call update_hunger after a successful move

    def draw(self, screen, font, tile_size):
        text_surface = font.render(self.smiley, True, self.color)
        # Convert grid coordinates to pixel coordinates for drawing
        pixel_x = self.x * tile_size
        pixel_y = self.y * tile_size
        screen.blit(text_surface, (pixel_x, pixel_y))
