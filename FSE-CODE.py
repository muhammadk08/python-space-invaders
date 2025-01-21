import pygame
from pygame import mixer
from random import randint

# Initialize Pygame
pygame.init()
mixer.init()

# Screen setup
SCREEN_WIDTH, SCREEN_HEIGHT = 1150, 850
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Space Invaders")

# Load assets
background = pygame.image.load("background.png")
background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))
logo = pygame.image.load("logo.png")
logo = pygame.transform.scale(logo, (500, 200))
space_ship1 = pygame.image.load("space_ship.png")
space_ship1 = pygame.transform.scale(space_ship1, (102, 108))
space_ship2 = pygame.image.load("space_ship2.png")
space_ship2 = pygame.transform.scale(space_ship2, (102, 108))
space_ship3 = pygame.image.load("space_ship3.png")
space_ship3 = pygame.transform.scale(space_ship3, (102, 108))
bullet = pygame.image.load("bullet.png")
bullet = pygame.transform.scale(bullet, (5, 20))
shield_img = pygame.image.load("shield.png")
shield_img = pygame.transform.scale(shield_img, (128, 96))
explosion_image = pygame.image.load("enemy_explosion.png")
explosion_image = pygame.transform.scale(explosion_image, (30, 30))

# Enemy sprites for animation
enemy_type1_frame1 = pygame.image.load("TopEnemy1.png")
enemy_type1_frame1 = pygame.transform.scale(enemy_type1_frame1, (55, 38))
enemy_type1_frame2 = pygame.image.load("TopEnemy2.png")
enemy_type1_frame2 = pygame.transform.scale(enemy_type1_frame2, (55, 38))

enemy_type2_frame1 = pygame.image.load("MiddleEnemy1.png")
enemy_type2_frame1 = pygame.transform.scale(enemy_type2_frame1, (55, 38))
enemy_type2_frame2 = pygame.image.load("MiddleEnemy2.png")
enemy_type2_frame2 = pygame.transform.scale(enemy_type2_frame2, (55, 38))

enemy_type3_frame1 = pygame.image.load("BottomEnemy1.png")
enemy_type3_frame1 = pygame.transform.scale(enemy_type3_frame1, (55, 38))
enemy_type3_frame2 = pygame.image.load("BottomEnemy2.png")
enemy_type3_frame2 = pygame.transform.scale(enemy_type3_frame2, (55, 38))

# Sounds
mixer.music.load("song.mp3")
mixer.music.play(-1)
shot_sound = mixer.Sound("shot.mp3")
Player_hit = mixer.Sound("Player_hit.mp3")
shield_hit = mixer.Sound("shield_hit.wav")
enemy_hit = mixer.Sound("enemy_hit.mp3")
click_sound = mixer.Sound("click.wav")

# Game variables
player_width, player_height = 102, 108
player_x, player_y = (SCREEN_WIDTH // 2) - (player_width // 2), SCREEN_HEIGHT - 150
player_speed = 9
player_lives = 3
score = 0
cooldown = 0
enemy_shots = []
player_shots = []
enemies = []  # To store enemy data: [rect, type, current_frame]
explosions = []  # To store explosions [x, y, duration]
enemy_direction = 1
enemy_speed = 3  # Adjusted speed for animation
enemy_drop = 20
enemy_shoot_rate = 1000  # Slower shoot rate for enemies
animation_timer = 0  # Timer for animation frames
animation_speed = 15  # Change frame every 15 ticks
active_ship = space_ship1  # Default spaceship
shield_positions = [(127, 550), (127 * 3, 550), (127 * 5, 550), (127 * 7, 550)]
shields = [shield_img.copy() for _ in shield_positions]
shield_health = [20, 20, 20, 20]  # Increased health for each shield

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
GRAY = (50, 50, 50)
# Font
font = pygame.font.SysFont("Courier New", 36)
# Game modes
game_mode = 0
menu_underline = {"x": 0, "y": 0, "size": 0}
# Global variable to store the player's name
player_name = "No Name Enterd"
# Add a global variable to track if the score has been saved
score_saved = False

def draw_text(surface, text, pos, color=WHITE):
    """Render text on the screen."""
    text_surface = font.render(text, True, color)
    surface.blit(text_surface, pos)

play_underline = {"x": 0, "y": 0, "size": 0}
instructions_underline = {"x": 0, "y": 0, "size": 0}
themes_underline = {"x": 0, "y": 0, "size": 0}
username_underline = {"x": 0, "y": 0, "size": 0}

def main_menu():
    """Display the main menu with individual underline animations."""
    global game_mode
    screen.blit(background, (0, 0))
    screen.blit(logo, (SCREEN_WIDTH // 2 - 250, 100))

    # Define button properties
    play_button = pygame.Rect(425, 350, 300, 60)
    instructions_button = pygame.Rect(425, 450, 300, 60)
    themes_button = pygame.Rect(425, 550, 300, 60)
    username_button = pygame.Rect(425, 650, 300, 60)

    global play_underline, instructions_underline, themes_underline, username_underline,score
    mx, my = pygame.mouse.get_pos()

    # Play button
    if play_button.collidepoint(mx, my):  # Mouse hover
        pygame.draw.rect(screen, GREEN, play_button, border_radius=30)
        pygame.draw.rect(screen, RED, play_button, width=5, border_radius=30)
        draw_text(screen, "Play", (525, 360), BLACK)
        # Expand underline
        if play_underline["x"] != play_button.x + play_button.width // 2:
            play_underline["size"] = 0
        play_underline["y"] = play_button.bottom - 15
        play_underline["x"] = play_button.x + play_button.width // 2
        if play_underline["size"] < play_button.width // 5:
            play_underline["size"] += 10
        if pygame.mouse.get_pressed()[0]:
            game_mode = 1
    else:
        pygame.draw.rect(screen, BLACK, play_button, border_radius=30)
        pygame.draw.rect(screen, RED, play_button, width=5, border_radius=30)
        draw_text(screen, "Play", (535, 360), WHITE)
        if play_underline["size"] > 0:
            play_underline["size"] -= 10

    # Instructions button
    if instructions_button.collidepoint(mx, my):
        pygame.draw.rect(screen, GREEN, instructions_button, border_radius=30)
        pygame.draw.rect(screen, RED, instructions_button, width=5, border_radius=30)
        draw_text(screen, "Instructions", (445, 460), BLACK)
        if instructions_underline["x"] != instructions_button.x + instructions_button.width // 2:
            instructions_underline["size"] = 0
        instructions_underline["y"] = instructions_button.bottom -15
        instructions_underline["x"] = instructions_button.x + instructions_button.width // 2
        if instructions_underline["size"] < instructions_button.width // 3+25:
            instructions_underline["size"] += 10
        if pygame.mouse.get_pressed()[0]:
            game_mode = 2
    else:
        pygame.draw.rect(screen, BLACK, instructions_button, border_radius=30)
        pygame.draw.rect(screen, RED, instructions_button, width=5, border_radius=30)
        draw_text(screen, "Instructions", (445+10, 460), WHITE)
        if instructions_underline["size"] > 0:
            instructions_underline["size"] -= 10

    # Themes button
    if themes_button.collidepoint(mx, my):
        pygame.draw.rect(screen, GREEN, themes_button, border_radius=30)
        pygame.draw.rect(screen, RED, themes_button, width=5, border_radius=30)
        draw_text(screen, "Themes", (510, 560), BLACK)
        if themes_underline["x"] != themes_button.x + themes_button.width // 2:
            themes_underline["size"] = 0
        themes_underline["y"] = themes_button.bottom-15
        themes_underline["x"] = themes_button.x + themes_button.width // 2
        if themes_underline["size"] < themes_button.width // 4-30:
            themes_underline["size"] += 10
        if pygame.mouse.get_pressed()[0]:
            game_mode = 3
    else:
        pygame.draw.rect(screen, BLACK, themes_button, border_radius=30)
        pygame.draw.rect(screen, RED, themes_button, width=5, border_radius=30)
        draw_text(screen, "Themes", (510+10, 560), WHITE)
        if themes_underline["size"] > 0:
            themes_underline["size"] -= 10

    # Username button
    if username_button.collidepoint(mx, my):
        pygame.draw.rect(screen, GREEN, username_button, border_radius=30)
        pygame.draw.rect(screen, RED, username_button, width=5, border_radius=30)
        draw_text(screen, "User Name", (475, 660), BLACK)
        if username_underline["x"] != username_button.x + username_button.width // 2:
            username_underline["size"] = 0
        username_underline["y"] = username_button.bottom-15
        username_underline["x"] = username_button.x + username_button.width // 2
        if username_underline["size"] < username_button.width // 3:
            username_underline["size"] += 10
        if pygame.mouse.get_pressed()[0]:
            game_mode = 5
    else:
        pygame.draw.rect(screen, BLACK, username_button, border_radius=30)
        pygame.draw.rect(screen, RED, username_button, width=5, border_radius=30)
        draw_text(screen, "User Name", (475+10, 660), WHITE)
        if username_underline["size"] > 0:
            username_underline["size"] -= 10

    # Draw underlines for all buttons
    pygame.draw.rect(
        screen, WHITE,
        (play_underline["x"] - play_underline["size"], play_underline["y"], play_underline["size"] * 2, 5),
        border_radius=15
    )
    pygame.draw.rect(
        screen, WHITE,
        (instructions_underline["x"] - instructions_underline["size"], instructions_underline["y"], instructions_underline["size"] * 2, 5),
        border_radius=15
    )
    pygame.draw.rect(
        screen, WHITE,
        (themes_underline["x"] - themes_underline["size"], themes_underline["y"], themes_underline["size"] * 2, 5),
        border_radius=15
    )
    pygame.draw.rect(
        screen, WHITE,
        (username_underline["x"] - username_underline["size"], username_underline["y"], username_underline["size"] * 2, 5),
        border_radius=15
    )

def username_screen():
    """Screen for entering the username."""
    global game_mode, player_name

    screen.fill(BLACK)
    draw_text(screen, "User Name Screen", (SCREEN_WIDTH // 2 - 200, 200), WHITE)

    # Define the "Enter Name" button
    enter_name_button = pygame.Rect(425, 350, 300, 60)

    # Get mouse position
    mx, my = pygame.mouse.get_pos()

    # Draw the Enter Name button
    if enter_name_button.collidepoint(mx, my):  # Hover effect
        pygame.draw.rect(screen, GREEN, enter_name_button, border_radius=30)
        pygame.draw.rect(screen, RED, enter_name_button, width=5, border_radius=30)
        draw_text(screen, "Enter Name", (485, 360), BLACK)
        if pygame.mouse.get_pressed()[0]:  # On click
            pygame.time.delay(200)  # Prevent multiple clicks
            player_name = input("Enter username: ").strip() or "No Name Entered"
    else:
        pygame.draw.rect(screen, BLACK, enter_name_button, border_radius=30)
        pygame.draw.rect(screen, RED, enter_name_button, width=5, border_radius=30)
        draw_text(screen, "Enter Name", (485, 360), WHITE)

    # Display the current name below the button
    draw_text(screen, f"Current Name: {player_name}", (SCREEN_WIDTH // 2 - 300, 450), WHITE)

    # Display back instructions
    draw_text(screen, "Press 'R' to Return to Main Menu", (SCREEN_WIDTH // 2 - 300, SCREEN_HEIGHT - 100), RED)

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:  # Return to main menu
                game_mode = 0

def play_game():
    """The main gameplay loop."""
    global player_x, player_y, player_lives, cooldown, animation_timer, enemies, score, running, active_ship,enemy_shoot_rate

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_x > 0:
        player_x -= player_speed
    if keys[pygame.K_RIGHT] and player_x < SCREEN_WIDTH - player_width:
        player_x += player_speed
    if keys[pygame.K_SPACE] and cooldown == 0:
        player_shots.append([player_x + player_width // 2, player_y])
        mixer.Sound.play(shot_sound)
        cooldown = 20

    move_enemies()
    move_bullets()
    shoot_enemy_bullets()

    # Update enemy animations
    animation_timer += 1
    if animation_timer >= animation_speed:
        for enemy in enemies:
            enemy[2] = 1 - enemy[2]  # Toggle between 0 and 1 for animation frames
        animation_timer = 0

    for enemy in enemies[:]:
        if detect_collision(enemy[0], player_shots):  # Check if an enemy is hit
            explosions.append((enemy[0].x, enemy[0].y, 15))  # Add explosion at enemy position
            enemies.remove(enemy)  # Remove the enemy
            mixer.Sound.play(enemy_hit)  # Play the enemy hit sound
            score += 10  # Increase the player's score
            # Increase enemy shooting rate, but keep it no less than 200
            if enemy_shoot_rate > 200:
                enemy_shoot_rate -=5


    for shot in enemy_shots[:]:
        if pygame.Rect(player_x, player_y, player_width, player_height).collidepoint(shot):
            enemy_shots.remove(shot)
            player_hit()

    for i in range(len(shields)):
        if shields[i]:  # Only weaken shields that still exist
            weaken_shield(i, enemy_shots)
            weaken_shield(i, player_shots)

    if len(enemies) == 0:
        reset_level()

    update_explosions()

    # Draw all elements
    screen.blit(background, (0, 0))
    screen.blit(active_ship, (player_x, player_y))  # Use the selected spaceship

    for enemy in enemies:
        rect, enemy_type, current_frame = enemy
        if enemy_type == 1:
            frame = enemy_type1_frame1 if current_frame == 0 else enemy_type1_frame2
        elif enemy_type == 2:
            frame = enemy_type2_frame1 if current_frame == 0 else enemy_type2_frame2
        else:
            frame = enemy_type3_frame1 if current_frame == 0 else enemy_type3_frame2
        screen.blit(frame, rect.topleft)

    for shot in player_shots:
        screen.blit(bullet, shot)
    for shot in enemy_shots:
        screen.blit(bullet, shot)
    for i, pos in enumerate(shield_positions):
        if shields[i]:
            screen.blit(shields[i], pos)

    draw_explosions()
    draw_text(screen, f"Score: {score}", (10, 10))
    draw_text(screen, f"Lives: {player_lives}", (SCREEN_WIDTH - 150, 10))


    cooldown = max(0, cooldown - 1)
def instructions():
    """Display the instructions screen."""
    screen.blit(background, (0, 0))
    
    # Display the title
    draw_text(screen, "Instructions", (SCREEN_WIDTH // 2 - 150, 100), WHITE)
    
    # Display the game instructions
    instructions_text = [
        "1. Use LEFT and RIGHT arrow keys to move your spaceship.",
        "2. Press SPACE to shoot bullets at enemies.",
        "3. Protect your shields and destroy enemies to score points.",
        "4. Avoid enemy bullets to save lives.",
        "5. Game ends when all lives are lost.",
    ]
    
    for i, line in enumerate(instructions_text):
        draw_text(screen, line, (100, 200 + i * 50), WHITE)
    
    # Back button instructions
    draw_text(screen, "Press 'R' to Return to the Main Menu", (100, SCREEN_HEIGHT - 100), RED)


def themes():
    """Display the themes screen and allow the user to select a spaceship."""
    global active_ship, game_mode

    screen.blit(background, (0, 0))
    draw_text(screen, "Select Your Spaceship", (SCREEN_WIDTH // 2 - 200, 50), WHITE)

    # Define spaceship buttons
    ship1_button = pygame.Rect(300, 300, 102, 108)
    ship2_button = pygame.Rect(525, 300, 102, 108)
    ship3_button = pygame.Rect(750, 300, 102, 108)

    mx, my = pygame.mouse.get_pos()

    # Draw spaceship buttons with hover effect
    pygame.draw.rect(screen, GREEN if ship1_button.collidepoint(mx, my) else RED, ship1_button, 2)
    pygame.draw.rect(screen, GREEN if ship2_button.collidepoint(mx, my) else RED, ship2_button, 2)
    pygame.draw.rect(screen, GREEN if ship3_button.collidepoint(mx, my) else RED, ship3_button, 2)

    # Display spaceship images
    screen.blit(space_ship1, (300, 300))
    screen.blit(space_ship2, (525, 300))
    screen.blit(space_ship3, (750, 300))

    # Handle clicks on spaceship buttons
    if pygame.mouse.get_pressed()[0]:
        if ship1_button.collidepoint(mx, my):
            active_ship = space_ship1
        elif ship2_button.collidepoint(mx, my):
            active_ship = space_ship2
        elif ship3_button.collidepoint(mx, my):
            active_ship = space_ship3

    # Display the selected spaceship under "My Ship"
    draw_text(screen, "My Ship", (SCREEN_WIDTH // 2 - 100, 500), WHITE)
    screen.blit(active_ship, (SCREEN_WIDTH // 2 - 51, 550))  # Centered below the "My Ship" text

    # Back button instructions
    draw_text(screen, "Press 'R' to Return to the Main Menu", (SCREEN_WIDTH // 2 - 200, SCREEN_HEIGHT - 100), RED)

    # Handle back button
    keys = pygame.key.get_pressed()
    if keys[pygame.K_r]:
        game_mode = 0



def reset_game():
    """Reset all game variables and restart everything for a fresh game."""
    global player_x, player_y, player_lives, score, cooldown, enemies, player_shots, enemy_shots, explosions, shield_health, shields, enemy_shoot_rate

    # Reset player position and lives
    player_x, player_y = (SCREEN_WIDTH // 2) - (player_width // 2), SCREEN_HEIGHT - 150
    player_lives = 3

    # Reset score and cooldown
    score = 0
    cooldown = 0

    # Clear gameplay elements
    enemies.clear()
    player_shots.clear()
    enemy_shots.clear()
    explosions.clear()

    # Reset shield health and images
    shield_health[:] = [20, 20, 20, 20]
    shields = [shield_img.copy() for _ in shield_positions]

    # Reset enemy shooting rate and reinitialize enemies
    enemy_shoot_rate = 1000  # Start with a slower shoot rate
    reset_level()  # Reset enemies and shields

def reset_score():
    """Reset the score when starting a new game."""
    global score
    score = 0

def endgame():
    """Display the endgame screen with final score and options."""
    global game_mode, running, player_name, score, score_saved

    # Draw the endgame screen
    screen.blit(background, (0, 0))
    draw_text(screen, "GAME OVER", (SCREEN_WIDTH // 2 - 150, 100), RED)
    draw_text(screen, f"Your Final Score: {score}", (SCREEN_WIDTH // 2 - 200, 200), WHITE)
    draw_text(screen, f"Player Name: {player_name}", (SCREEN_WIDTH // 2 - 200, 250), WHITE)

    # Save the player's score to a file if it hasn't been saved yet
    if not score_saved:
        with open("leaderboard.txt", "a") as file:
            file.write(f"{player_name}, {score}\n")

        # Read the leaderboard, sort it, and save the updated list back
        with open("leaderboard.txt", "r") as file:
            entries = [
                line.strip().split(", ") for line in file.readlines()
                if len(line.strip().split(", ")) == 2
            ]
        sorted_entries = sorted(entries, key=lambda x: int(x[1]), reverse=True)  # Sort by score, descending
        with open("leaderboard.txt", "w") as file:
            for name, score in sorted_entries:
                file.write(f"{name}, {score}\n")
        
        score_saved = True  # Mark as saved to prevent repeated saving

    # Buttons for Restart and Main Menu
    restart_button = pygame.Rect(425, 350, 300, 60)
    menu_button = pygame.Rect(425, 450, 300, 60)
    mx, my = pygame.mouse.get_pos()

    # Restart Button
    if restart_button.collidepoint(mx, my):
        pygame.draw.rect(screen, GREEN, restart_button, border_radius=30)
        pygame.draw.rect(screen, RED, restart_button, width=5, border_radius=30)
        draw_text(screen, "Restart", (525, 360), BLACK)
        if pygame.mouse.get_pressed()[0]:
            pygame.time.delay(200)  # Prevent multiple clicks
            reset_game()  # Restart the game with reset variables
            score_saved = False  # Reset the save flag for the next game
            game_mode = 1
    else:
        pygame.draw.rect(screen, BLACK, restart_button, border_radius=30)
        pygame.draw.rect(screen, RED, restart_button, width=5, border_radius=30)
        draw_text(screen, "Restart", (525, 360), WHITE)

    # Main Menu Button
    if menu_button.collidepoint(mx, my):
        pygame.draw.rect(screen, GREEN, menu_button, border_radius=30)
        pygame.draw.rect(screen, RED, menu_button, width=5, border_radius=30)
        draw_text(screen, "Main Menu", (465, 460), BLACK)
        if pygame.mouse.get_pressed()[0]:
            pygame.time.delay(200)  # Prevent multiple clicks
            reset_game()  # Reset game variables
            reset_score()  # Reset the score for a fresh start
            score_saved = False  # Reset the save flag for the next game
            game_mode = 0
    else:
        pygame.draw.rect(screen, BLACK, menu_button, border_radius=30)
        pygame.draw.rect(screen, RED, menu_button, width=5, border_radius=30)
        draw_text(screen, "Main Menu", (465, 460), WHITE)


def draw_text(surface,text, pos,color=WHITE):
    """Render text on the screen."""
    text_surface = font.render(text, True, color)
    surface.blit(text_surface, pos)

def reset_level():
    """Reset enemies and shields for a new level."""
    global enemies, enemy_shoot_rate, shield_health, shields

    # Reset enemies
    enemies.clear()
    enemy_shoot_rate = max(50, enemy_shoot_rate - 20)  # Gradually increase shooting rate

    # Reinitialize enemies
    for y, enemy_type in [(100, 1), (150, 1), (200, 2), (250, 2), (300, 3), (350, 3)]:
        for x in range(150, 851, 70):
            enemies.append([pygame.Rect(x, y, 55, 38), enemy_type, 0])

    # Reset shields
    shield_health[:] = [20, 20, 20, 20]  # Reset shield health
    shields = [shield_img.copy() for _ in shield_positions]  # Restore the shield images


def move_enemies():
    """Move enemies horizontally and drop them when they hit the edges."""
    global enemy_direction
    hit_edge = False
    for enemy in enemies:
        enemy[0].x += enemy_direction * enemy_speed
        if enemy[0].right >= SCREEN_WIDTH or enemy[0].left <= 0:
            hit_edge = True
    if hit_edge:
        enemy_direction *= -1
        for enemy in enemies:
            enemy[0].y += enemy_drop

def shoot_enemy_bullets():
    """Randomly generate enemy bullets based on current shoot rate."""
    for enemy in enemies:
        if randint(1, enemy_shoot_rate) == 1:
            enemy_shots.append([enemy[0].centerx, enemy[0].bottom])

def move_bullets():
    """Move player and enemy bullets."""
    for shot in player_shots[:]:
        shot[1] -= 40  # Faster player bullets
        if shot[1] < 0:
            player_shots.remove(shot)
    for shot in enemy_shots[:]:
        shot[1] += 10  # Faster enemy bullets
        if shot[1] > SCREEN_HEIGHT:
            enemy_shots.remove(shot)

def detect_collision(rect, shots):
    """Check for collisions between a rectangle and bullets."""
    for shot in shots:
        if rect.collidepoint(shot):
            shots.remove(shot)
            return True
    return False

def player_hit():
    """Handle player getting hit by an enemy bullet."""
    global player_lives, running, game_mode
    mixer.Sound.play(Player_hit)
    player_lives -= 1  # Decrease player's lives
    if player_lives <= 0:
        game_mode = 4  # Switch to game over mode


def weaken_shield(shield_index, shots):
    """Reduce shield size and health upon collision with a bullet."""
    if shields[shield_index] is None:  # Skip processing if the shield has already been removed
        return

    shield_rect = shields[shield_index].get_rect(topleft=shield_positions[shield_index])
    for shot in shots[:]:
        if shield_rect.collidepoint(shot):  # Check if the shield is hit
            shots.remove(shot)
            mixer.Sound.play(shield_hit)  # Play the shield hit sound
            shield_health[shield_index] -= 1
            width, height = shields[shield_index].get_size()
            # Remove a random chunk of the shield to simulate damage
            shields[shield_index].fill((0, 0, 0), pygame.Rect(randint(0, width - 20), randint(0, height - 20), 20, 20))

            # Remove the shield if health reaches 0
            if shield_health[shield_index] <= 0:
                shields[shield_index] = None

def draw_explosions():
    """Draw explosions on the screen."""
    for explosion in explosions:
        screen.blit(explosion_image, (explosion[0], explosion[1]))

def update_explosions():
    """Update explosion durations and remove expired ones."""
    global explosions
    explosions = [(x, y, duration - 1) for x, y, duration in explosions if duration > 0]
# Game loop
running = True
reset_level()
while running:
    screen.fill((0, 0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r and game_mode in [2, 5, 3]:
                mixer.Sound.play(click_sound)
                game_mode = 0  # Return to main menu
        if event.type == pygame.MOUSEBUTTONDOWN:  # Mouse click event
            mixer.Sound.play(click_sound)

    if game_mode == 0:
        main_menu()  # All button handling is inside this function now
    elif game_mode == 1:
        play_game()
    elif game_mode == 2:
        instructions()
    elif game_mode == 3:
        themes()
    elif game_mode == 4:
        endgame()
    elif game_mode == 5:
        username_screen()
    
    pygame.display.flip()
    pygame.time.delay(30)

pygame.quit()
