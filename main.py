import pygame
import random

# Initialize Pygame
pygame.init()

# Set the screen dimensions
screen_width = 800
screen_height = 600

# Create the game window
screen = pygame.display.set_mode((screen_width, screen_height))

# Set the title of the game window
pygame.display.set_caption('Alien Shooter')

# Load the background image
background = pygame.image.load('background.jpg')

# Load the player image
player = pygame.image.load('player.png')
player_width = player.get_width()
player_height = player.get_height()

# Set the initial position of the player
player_x = (screen_width - player_width) / 2
player_y = screen_height - player_height - 10

# Set the speed of the player
player_speed = 5

# Load the bullet image
bullet = pygame.image.load('bullet.png')
bullet_width = bullet.get_width()
bullet_height = bullet.get_height()

# Create a list to store the bullets
bullets = []

# Set the speed of the bullets
bullet_speed = 7

# Load the alien image
alien = pygame.image.load('alien.png')
alien_width = alien.get_width()
alien_height = alien.get_height()

# Create a list to store the aliens
aliens = []

# Set the speed of the aliens
alien_speed = 2

# Set the frequency of the aliens
alien_frequency = 100

# Set the score to zero
score = 0

# Load the font for the score display
font = pygame.font.Font(None, 30)

# Set the game clock
clock = pygame.time.Clock()


# Define a function to draw the player
def draw_player():
    screen.blit(player, (player_x, player_y))


# Define a function to move the player
def move_player(direction):
    global player_x, player_speed
    if direction == 'left':
        player_x -= player_speed
    elif direction == 'right':
        player_x += player_speed
    # Keep the player within the screen bounds
    if player_x < 0:
        player_x = 0
    elif player_x > screen_width - player_width:
        player_x = screen_width - player_width


# Define a function to handle key presses
def handle_key_presses(keys):
    global player_x, player_speed, bullets, last_bullet_time
    if keys[pygame.K_LEFT]:
        player_speed -= 0.5
        if player_speed < 1:
            player_speed = 5
        move_player('left')
    elif keys[pygame.K_RIGHT]:
        player_speed -= 0.5
        if player_speed < 1:
            player_speed = 5
        move_player('right')
    else:
        player_speed = 5

    current_time = pygame.time.get_ticks()
    if keys[pygame.K_SPACE] and current_time - last_bullet_time > 500:
        bullets.append((player_x + player_width / 2 - bullet_width / 2, player_y - bullet_height))
        last_bullet_time = current_time


# Define a function to draw the bullets
def draw_bullets():
    for bullet_x, bullet_y in bullets:
        screen.blit(bullet, (bullet_x, bullet_y))


# Define a function to move the bullets
def move_bullets():
    global bullets
    new_bullets = []
    for bullet_x, bullet_y in bullets:
        bullet_y -= bullet_speed
        if bullet_y > 0:
            new_bullets.append((bullet_x, bullet_y))
    bullets = new_bullets


# Define a function to draw the aliens
def draw_aliens():
    for alien_x, alien_y in aliens:
        screen.blit(alien, (alien_x, alien_y))


# Define a function to move the aliens
def move_aliens():
    global aliens, score
    new_aliens = []
    for alien_x, alien_y in aliens:
        alien_y += alien_speed
        if alien_y < screen_height:
            new_aliens.append((alien_x, alien_y))
        else:
            # Alien has reached the bottom of the screen
            score -= 10
    aliens = new_aliens


# Define a function to spawn aliens
def spawn_aliens():
    global aliens
    if random.randint(1, alien_frequency) == 1:
        alien_x = random.randint(0, screen_width - alien_width)
        alien_y = -alien_height
        aliens.append((alien_x, alien_y))


# Define a function to check for collisions
def check_collisions():
    global bullets, aliens, score
    new_bullets = []
    for bullet in bullets:
        bullet_x, bullet_y = bullet
        hit = False
        for alien in aliens:
            alien_x, alien_y = alien
            if ((bullet_x >= alien_x and bullet_x <= alien_x + alien_width) or
                    (bullet_x + bullet_width >= alien_x and bullet_x + bullet_width <= alien_x + alien_width)):
                if bullet_y <= alien_y + alien_height and bullet_y >= alien_y:
                    # Bullet has hit an alien
                    score += 10
                    aliens.remove(alien)
                    hit = True
                    break
        if not hit:
            new_bullets.append(bullet)
    aliens_hit_player = False
    for alien in aliens:
        alien_x, alien_y = alien
        if ((alien_x >= player_x and alien_x <= player_x + player_width) or
                (alien_x + alien_width >= player_x and alien_x + alien_width <= player_x + player_width)):
            if alien_y + alien_height >= player_y:
                # Player has been hit by an alien
                aliens_hit_player = True
                break
    if aliens_hit_player:
        return True
    else:
        bullets = new_bullets
        return False


# Define the main game loop
def game_loop():
    global player_x, player_y, bullets, aliens, score, last_bullet_time
    last_bullet_time = 0
    game_over = False
    while not game_over:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True

        # Handle key presses
        keys = pygame.key.get_pressed()
        handle_key_presses(keys)

        # Spawn aliens
        spawn_aliens()

        # Move and draw objects
        move_bullets()
        move_aliens()
        screen.fill((0, 0, 0)) # Clear the screen
        draw_player()
        draw_bullets()
        draw_aliens()

        # Check for collisions
        if check_collisions():
            game_over = True

        # Draw the score
        score_text = font.render('Score: {}'.format(score), True, (255, 255, 255))
        screen.blit(score_text, (10, 10))

        # Update the screen
        pygame.display.update()

        # Set the game clock speed
        clock.tick(60)

    # Clean up resources
    pygame.quit()


# Run the game loop
game_loop()
