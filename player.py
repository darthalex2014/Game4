import pygame
# import main # For accessing main.message_log - REMOVED

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
        self.inventory = []
        self.max_inventory_size = 10
        self.attack_power = 10 # Player's attack power

    def update_hunger(self):
        self.hunger -= 1
        if self.hunger < 0:
            self.hunger = 0
        
        if self.hunger == 0:
            # Apply penalty for starvation
            self.health -= 1 # Direct modification for now
            if self.health < 0:
                self.health = 0
            # Optionally add message for starving:
            # message_log.add_message("You are starving!", (255,100,100)) # Example if message_log is passed here


    def eat_food(self, food_item, message_log): # Added message_log parameter
        if food_item in self.inventory:
            self.hunger += food_item.hunger_value
            if self.hunger > self.max_hunger:
                self.hunger = self.max_hunger
            self.inventory.remove(food_item)
            message_log.add_message(f"You ate the {food_item.name}.", (0, 255, 0))
        else:
            message_log.add_message(f"Cannot eat {food_item.name}, not in inventory.", (255,255,0))


    def take_damage(self, damage, message_log): # Added message_log parameter
        self.health -= damage
        if self.health <= 0:
            self.health = 0
            self.is_dead = True 
            message_log.add_message("You died!", (255, 0, 0)) # Red color for death

    def move(self, dx, dy, game_map, enemies, message_log): # Added message_log parameter
        new_x = self.x + dx
        new_y = self.y + dy

        # Check for enemy at the target location
        for enemy in enemies:
            if not enemy.is_dead and enemy.x == new_x and enemy.y == new_y:
                message_log.add_message(f"You attack the {enemy.name} for {self.attack_power} damage.", (0, 200, 255)) # Light blue for player attack
                enemy.take_damage(self.attack_power, message_log) # Pass message_log to enemy's take_damage
                self.update_hunger() 
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
