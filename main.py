import pygame
from player import Player # Import the Player class
from map import Map # Import the Map class
from enemy import Enemy # Import the Enemy class
from items import Item, Food # Import Item and Food classes
from message_log import MessageLog # Import MessageLog

# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GOBLIN_COLOR = (0, 128, 0)  # Dark Green
ORC_COLOR = (139, 69, 19)   # Brown (SaddleBrown)

# Set screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600 # Adjusted to 19 * 32 = 608, or keep 600 and have a small bottom margin
TILE_SIZE = 32 # Define TILE_SIZE

# Map dimensions
MAP_WIDTH = SCREEN_WIDTH // TILE_SIZE  # 25 tiles
MAP_HEIGHT = SCREEN_HEIGHT // TILE_SIZE # 18.75, so effectively 18 or 19. Let's use 19.
# SCREEN_HEIGHT = MAP_HEIGHT * TILE_SIZE # Optional: Adjust screen height to perfectly fit map

# Initialize Pygame
pygame.init()

# Create the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Set window caption
pygame.display.set_caption("Roguelike Game")

# Font setup
game_font = pygame.font.Font(None, TILE_SIZE) # Using TILE_SIZE for font size for consistency

# Create map instance (now determines player start)
game_map = Map(MAP_WIDTH, MAP_HEIGHT)

# Create player instance using map's determined start position
player = Player(x=game_map.player_start_x, y=game_map.player_start_y, smiley='@')

# Create enemies list
enemies = []
initial_enemies_spawned = False 
# enemy_color = (255, 0, 0) # Old generic enemy color - REMOVED

# Spawn enemies in random rooms
num_enemies_to_spawn = 3 
if game_map.rooms: 
    for _ in range(num_enemies_to_spawn):
        placed_enemy = False
        for _ in range(100): # Attempt to place each enemy 100 times
            room = random.choice(game_map.rooms)
            enemy_x = random.randint(room.x1, room.x2 - 1)
            enemy_y = random.randint(room.y1, room.y2 - 1)

            if game_map.is_walkable(enemy_x, enemy_y) and \
               not (enemy_x == player.x and enemy_y == player.y): 
                occupied_by_another_enemy = False
                for e in enemies:
                    if e.x == enemy_x and e.y == enemy_y:
                        occupied_by_another_enemy = True
                        break
                if not occupied_by_another_enemy:
                    # Randomly choose between Goblin and Orc
                    if random.random() < 0.5: # 50% chance for Orc
                        # Orc: smiley 'O', health 40, ORC_COLOR, attack 8, vision 4, name "Orc"
                        enemies.append(Enemy(enemy_x, enemy_y, 'O', 40, ORC_COLOR, 8, 4, "Orc"))
                    else:
                        # Goblin: smiley 'G', health 20, GOBLIN_COLOR, attack 5, vision 5, name "Goblin"
                        enemies.append(Enemy(enemy_x, enemy_y, 'G', 20, GOBLIN_COLOR, 5, 5, "Goblin"))
                    placed_enemy = True
                    break # Successfully placed this enemy
        if not placed_enemy:
            print(f"Warning: Could not place an enemy after 100 attempts.")

if enemies: 
    initial_enemies_spawned = True


# Game state
game_state = "playing"
previous_game_state = "playing" # To store state before help screen

# Initialize Message Log
message_log = MessageLog()
message_log.add_message("Welcome to the Dungeon!", (0, 255, 0)) # Initial welcome message

# Initial values for reset
PLAYER_INITIAL_SMILEY = '@'
# ENEMY_INITIAL_SMILEY = 'E' # REMOVED
# ENEMY_INITIAL_HEALTH = 25 # REMOVED

def reset_game():
    global player, enemies, game_state, initial_enemies_spawned, game_map, message_log # Added game_map and message_log
    
    # Regenerate the map layout (this will also reset player_start_x/y on map, and items)
    game_map._generate_dungeon() 

    # Re-initialize player to the new map's start position and reset stats
    player.__init__(game_map.player_start_x, game_map.player_start_y, PLAYER_INITIAL_SMILEY)

    # Reset enemies
    enemies.clear()
    initial_enemies_spawned = False
    num_enemies_to_spawn = 3 # Same as initial spawn
    if game_map.rooms:
        for _ in range(num_enemies_to_spawn):
            placed_enemy = False
            for _ in range(100): # Attempt to place each enemy
                room = random.choice(game_map.rooms)
                enemy_x = random.randint(room.x1, room.x2 - 1)
                enemy_y = random.randint(room.y1, room.y2 - 1)
                if game_map.is_walkable(enemy_x, enemy_y) and \
                   not (enemy_x == player.x and enemy_y == player.y):
                    occupied_by_another_enemy = False
                    for e in enemies:
                        if e.x == enemy_x and e.y == enemy_y:
                            occupied_by_another_enemy = True
                            break
                    if not occupied_by_another_enemy:
                        # Randomly choose between Goblin and Orc for reset as well
                        if random.random() < 0.5: # 50% chance for Orc
                            enemies.append(Enemy(enemy_x, enemy_y, 'O', 40, ORC_COLOR, 8, 4, "Orc"))
                        else:
                            enemies.append(Enemy(enemy_x, enemy_y, 'G', 20, GOBLIN_COLOR, 5, 5, "Goblin"))
                        placed_enemy = True
                        break # Successfully placed this enemy
            if not placed_enemy:
                print(f"Warning: Could not place an enemy after 100 attempts during reset.")
    
    if enemies:
        initial_enemies_spawned = True

    # game_map.items is already cleared and re-placed by _generate_dungeon -> _place_items

    # Reset game state
    game_state = "playing"
    # print("Game has been reset.") # Old print
    message_log.messages.clear()
    message_log.add_message("Welcome to the Dungeon!", (0, 255, 0))


# Game loop
running = True
clock = pygame.time.Clock()

while running:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if game_state == "playing":
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    player.move(0, -1, game_map, enemies, message_log) # Pass message_log
                elif event.key == pygame.K_DOWN:
                    player.move(0, 1, game_map, enemies, message_log) # Pass message_log
                elif event.key == pygame.K_LEFT:
                    player.move(-1, 0, game_map, enemies, message_log) # Pass message_log
                elif event.key == pygame.K_RIGHT:
                    player.move(1, 0, game_map, enemies, message_log) # Pass message_log
                # elif event.key == pygame.K_e: # Old Test eating - REMOVED
                #    player.eat(20) 
                elif event.key == pygame.K_h: # Toggle Help Screen
                    previous_game_state = game_state
                    game_state = "help"
                elif event.key == pygame.K_i: # Toggle Inventory Screen
                    previous_game_state = game_state
                    game_state = "show_inventory"


        elif game_state == "help":
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE or event.key == pygame.K_h:
                    game_state = previous_game_state

        elif game_state == "show_inventory":
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE or event.key == pygame.K_i:
                    game_state = previous_game_state
                # Check for number keys 1-9 to eat food
                elif event.unicode.isdigit() and int(event.unicode) > 0:
                    item_index = int(event.unicode) - 1
                    if item_index < len(player.inventory):
                        selected_item = player.inventory[item_index]
                        if isinstance(selected_item, Food):
                            player.eat_food(selected_item, message_log) # Pass message_log
                            # game_state = previous_game_state # Optionally switch back after eating
                        else:
                            # print(f"{selected_item.name} is not edible.") # Old print
                            message_log.add_message(f"{selected_item.name} is not edible.", (255,255,0))
                    else:
                        # print("Invalid inventory number.") # Old print
                        message_log.add_message("Invalid inventory number.", (255,255,0))
        
        elif game_state == "game_over" or game_state == "victory":
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_r:
                    reset_game()


    if game_state == "playing":
        # Item Pickup Logic (after player has moved)
        for item in list(game_map.items): # Iterate a copy for safe removal
            if player.x == item.x and player.y == item.y:
                if len(player.inventory) < player.max_inventory_size:
                    player.inventory.append(item)
                    game_map.items.remove(item)
                    # print(f"Player picked up {item.name}.") # Old print
                    message_log.add_message(f"You picked up {item.name}.", (0, 255, 255)) # Cyan for item pickup
                else:
                    # print("Inventory is full!") # Old print
                    message_log.add_message("Inventory is full!", (255, 255, 0)) # Yellow for warning
                break # Assuming one item per tile

        # Enemy turn
        for enemy in enemies:
            if not enemy.is_dead:
                enemy.move(player.x, player.y, game_map, player, message_log) # Pass message_log

        # Remove dead enemies
        enemies = [enemy for enemy in enemies if not enemy.is_dead]

        # Check for game over condition
        if player.is_dead:
            game_state = "game_over"
        
        # Check for win condition
        if not enemies and initial_enemies_spawned:
            game_state = "victory"

    # Drawing operations
    screen.fill(BLACK)
    game_map.draw(screen, game_font, TILE_SIZE)
    
    # Draw enemies first
    for enemy in enemies: # Will be empty in victory state after filtering
        enemy.draw(screen, game_font, TILE_SIZE)
    
    # Draw player (even if dead, to show final position)
    player.draw(screen, game_font, TILE_SIZE)

    # UI Text Rendering (Health and Hunger)
    health_text = f"Health: {player.health}/{player.max_health}"
    health_surface = game_font.render(health_text, True, WHITE)
    screen.blit(health_surface, (10, 10))

    hunger_text = f"Hunger: {player.hunger}/{player.max_hunger}"
    hunger_surface = game_font.render(hunger_text, True, WHITE)
    screen.blit(hunger_surface, (10, 10 + TILE_SIZE // 2 + 5))

    # Game Over / Victory Messages
    if game_state == "game_over":
        msg_text = "GAME OVER"
        msg_surface = game_font.render(msg_text, True, (255, 0, 0)) # Red color
        msg_rect = msg_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        screen.blit(msg_surface, msg_rect)
        
        instr_text = "Press R to Restart or ESC to Quit"
        instr_surface = game_font.render(instr_text, True, WHITE)
        instr_rect = instr_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + TILE_SIZE))
        screen.blit(instr_surface, instr_rect)

    elif game_state == "victory":
        msg_text = "YOU WIN!"
        msg_surface = game_font.render(msg_text, True, (0, 255, 0)) # Green color
        msg_rect = msg_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        screen.blit(msg_surface, msg_rect)

        instr_text = "Press R to Restart or ESC to Quit"
        instr_surface = game_font.render(instr_text, True, WHITE)
        instr_rect = instr_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + TILE_SIZE))
        screen.blit(instr_surface, instr_rect)

    elif game_state == "help":
        # Optional: Draw a semi-transparent overlay or solid background
        help_bg_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        help_bg_surface.fill(BLACK) # Solid black background
        help_bg_surface.set_alpha(230) # Semi-transparent
        screen.blit(help_bg_surface, (0,0))

        help_texts = [
            "--- HOW TO PLAY ---",
            "",
            "Controls:",
            "  Arrow Keys: Move Player / Attack Enemy",
            "  'I': Open/Close Inventory",
            "  'H': Toggle this Help Screen",
            "",
            "Goal: Defeat all enemies!", # Changed from ('E')
            "",
            "Symbols:",
            "  '@': You (The Player)",
            "  'G': Goblin",
            "  'O': Orc",
            "  '#': Wall",
            "  '.': Floor",
            "",
            "UI:",
            "  Health: Your current health. If it reaches 0, you die.",
            "  Hunger: Your current hunger. Decreases as you move.",
            "          If it reaches 0, you lose health.",
            "",
            "In Inventory ('I'):",
            "  Press number (1-9) to eat corresponding food item.",
            "  'I' or ESC to close inventory.",
            "",
            "Press 'H' or ESC to return to game."
        ]
        
        line_height = game_font.get_linesize()
        start_x = 50
        start_y = 50

        for i, line in enumerate(help_texts):
            text_surface = game_font.render(line, True, WHITE)
            screen.blit(text_surface, (start_x, start_y + i * line_height))

    elif game_state == "show_inventory":
        # Optional: Draw a semi-transparent overlay or solid background
        inv_bg_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        inv_bg_surface.fill(BLACK) 
        inv_bg_surface.set_alpha(230) 
        screen.blit(inv_bg_surface, (0,0))

        inv_texts = ["--- INVENTORY ---"]
        if not player.inventory:
            inv_texts.append("Your inventory is empty.")
        else:
            for i, item_obj in enumerate(player.inventory):
                item_type = "Food" if isinstance(item_obj, Food) else "Item"
                inv_texts.append(f"{i+1}: {item_obj.name} ({item_type}) - Smiley: {item_obj.smiley}")
        
        inv_texts.append("")
        inv_texts.append("Press number (1-9) to use/eat food.")
        inv_texts.append("Press 'I' or ESC to close.")
        
        line_height = game_font.get_linesize()
        start_x = 50
        start_y = 50

        for i, line in enumerate(inv_texts):
            text_surface = game_font.render(line, True, WHITE)
            screen.blit(text_surface, (start_x, start_y + i * line_height))

    # Draw Message Log
    msg_log_y_start = SCREEN_HEIGHT - (message_log.max_messages * game_font.get_linesize()) - 10
    msg_x = 10
    for i, msg_dict in enumerate(message_log.get_display_messages()):
        msg_surface = game_font.render(msg_dict['text'], True, msg_dict['color'])
        screen.blit(msg_surface, (msg_x, msg_log_y_start + i * game_font.get_linesize()))


    pygame.display.flip()
    clock.tick(15) # Changed FPS from 60 to 15

# Quit Pygame
pygame.quit()
