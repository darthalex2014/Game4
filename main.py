import pygame
from player import Player # Import the Player class
from map import Map # Import the Map class
from enemy import Enemy # Import the Enemy class

# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

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

# Create map instance
game_map = Map(MAP_WIDTH, MAP_HEIGHT)

# Create player instance
# Ensure player starts on a walkable tile, e.g., center of the map
player_start_x = MAP_WIDTH // 2
player_start_y = MAP_HEIGHT // 2
player = Player(x=player_start_x, y=player_start_y, smiley='@')

# Create enemies list
enemies = []
initial_enemies_spawned = False # Flag to track if enemies were spawned
enemy_color = (255, 0, 0) # Red for enemies

# Spawn enemies at valid locations
enemy_positions = [(3, 3), (MAP_WIDTH - 4, MAP_HEIGHT - 4), (3, MAP_HEIGHT - 4)]
# Ensure at least one enemy spawns for testing win condition, adjust if needed
if not enemies: # Attempt to spawn if list is empty
    for pos_x, pos_y in enemy_positions:
        if game_map.is_walkable(pos_x, pos_y) and not (pos_x == player_start_x and pos_y == player_start_y):
            enemies.append(Enemy(pos_x, pos_y, 'E', 25, enemy_color))
        # Fallback if preset positions are not ideal
        elif game_map.is_walkable(player_start_x + 2, player_start_y + 2) and not (player_start_x + 2 == player_start_x and player_start_y + 2 == player_start_y):
             enemies.append(Enemy(player_start_x + 2, player_start_y + 2, 'E', 25, enemy_color))
             # Break after first successful fallback to ensure not too many enemies from fallback
             if len(enemies) >= 1: break 

if enemies: # If any enemies were added
    initial_enemies_spawned = True


# Game state
game_state = "playing"

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
                    player.move(0, -1, game_map, enemies)
                elif event.key == pygame.K_DOWN:
                    player.move(0, 1, game_map, enemies)
                elif event.key == pygame.K_LEFT:
                    player.move(-1, 0, game_map, enemies)
                elif event.key == pygame.K_RIGHT:
                    player.move(1, 0, game_map, enemies)
                elif event.key == pygame.K_e: # Test eating
                    player.eat(20)
        elif game_state == "game_over" or game_state == "victory":
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                # Optionally, add a restart key like R
                # if event.key == pygame.K_r:
                #    # Reset game (re-initialize player, enemies, map, game_state)
                #    # This would require a function to reset the game state
                #    pass


    if game_state == "playing":
        # Enemy turn
        for enemy in enemies:
            if not enemy.is_dead:
                enemy.move(player.x, player.y, game_map, player)

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
        
        instr_text = "Press ESC to quit"
        instr_surface = game_font.render(instr_text, True, WHITE)
        instr_rect = instr_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + TILE_SIZE))
        screen.blit(instr_surface, instr_rect)

    elif game_state == "victory":
        msg_text = "YOU WIN!"
        msg_surface = game_font.render(msg_text, True, (0, 255, 0)) # Green color
        msg_rect = msg_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        screen.blit(msg_surface, msg_rect)

        instr_text = "Press ESC to quit"
        instr_surface = game_font.render(instr_text, True, WHITE)
        instr_rect = instr_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + TILE_SIZE))
        screen.blit(instr_surface, instr_rect)

    pygame.display.flip()
    clock.tick(60) # Assuming FPS is 60

# Quit Pygame
pygame.quit()
