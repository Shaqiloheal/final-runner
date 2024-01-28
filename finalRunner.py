# Import necessary libraries
import pygame
from sys import exit
from random import randint


def display_score():
    current_time = int(pygame.time.get_ticks() / 1000) - start_time
    score_surface = test_font.render(f'Score: {current_time}', False, (64, 64, 64))
    score_rect = score_surface.get_rect(center=(400, 50))
    screen.blit(score_surface, score_rect)
    return current_time


def obstacle_movement(obstacle_list):
    if obstacle_list:
        for obstacle_rect in obstacle_list:
            obstacle_rect.x -= 5

            if obstacle_rect.bottom == 300:
                screen.blit(snail_surface, obstacle_rect)
            else:
                screen.blit(fly_surface, obstacle_rect)

        obstacle_list = [obstacle for obstacle in obstacle_list if obstacle.x > -100]

        return obstacle_list
    else:
        return []


def collisions(player, obstacles):
    if obstacles:
        for obstacle_rect in obstacles:
            if player.colliderect(obstacle_rect):
                return False
    return True


# Initialise Pygame
pygame.init()

# Set up the display window
screen = pygame.display.set_mode((800, 400))
pygame.display.set_caption('Final Runner')
clock = pygame.time.Clock()
game_active = False
start_time = 0
score = 0

# Load font for text rendering
test_font = pygame.font.Font('font/Pixeltype.ttf', 50)

# Load background images and convert them for optimal performance
sky_surface = pygame.image.load('graphics/Sky.png').convert()
ground_surface = pygame.image.load('graphics/ground.png').convert()

# Obstacles
# Load snail image, enable transparency, and set its initial position
snail_surface = pygame.image.load('graphics/snail/snail1.png').convert_alpha()
fly_surface = pygame.image.load('graphics/Fly/Fly1.png').convert_alpha()

obstacle_rect_list = []

# Load player image, enable transparency, and set initial position and gravity
player_surface = pygame.image.load('graphics/Player/player_walk_1.png').convert_alpha()
player_rect = player_surface.get_rect(midbottom=(80, 300))
player_gravity = 0

# Intro Screen
player_stand = pygame.image.load('graphics/Player/player_stand.png').convert_alpha()
player_stand = pygame.transform.rotozoom(player_stand, 0, 2)
player_stand_rect = player_stand.get_rect(center=(400, 200))

title_surface = test_font.render('Final Runner', False, (111, 196, 169))
title_rect = title_surface.get_rect(center=(400, 80))

game_message = test_font.render('Press SPACE to run!', False, (111, 196, 169))
game_message_rect = game_message.get_rect(center=(400, 320))

game_over_message = test_font.render(f'GAME OVER!', False, (111, 196, 169))
game_over_rect = game_over_message.get_rect(center=(400, 320))

# Timer
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 1500)

# Main game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if game_active:
            # Player jumps if mouse button
            if event.type == pygame.MOUSEBUTTONDOWN and player_rect.bottom >= 300:
                if player_rect.collidepoint(event.pos):
                    player_gravity = -20

            # Player jumps if SPACE key is pressed
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and player_rect.bottom >= 300:
                    player_gravity = -20
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                start_time = int(pygame.time.get_ticks() / 1000)
                game_active = True

        if event.type == obstacle_timer and game_active:
            if randint(0, 2):
                obstacle_rect_list.append(snail_surface.get_rect(bottomright=(randint(900, 1100), 300)))
            else:
                obstacle_rect_list.append(fly_surface.get_rect(bottomright=(randint(900, 1100), 210)))

    if game_active:

        # Draw background images
        screen.blit(sky_surface, (0, 0))
        screen.blit(ground_surface, (0, 300))

        # Draw and position the score text
        # pygame.draw.rect(screen, '#c0e8ec', score_rect)
        # pygame.draw.rect(screen, '#c0e8ec', score_rect, 10)
        # screen.blit(score_surface, score_rect)
        score = display_score()

        # Snail
        # Move the snail and reset its position if it goes off-screen
        # snail_rect.x -= 4
        # if snail_rect.right <= 0:
        #     snail_rect.left = 800
        # screen.blit(snail_surface, snail_rect)

        # Player
        # Apply gravity to the player and ensure they land on the ground
        player_gravity += 1
        player_rect.y += player_gravity
        if player_rect.bottom >= 300:
            player_rect.bottom = 300
        screen.blit(player_surface, player_rect)

        # Obstacle movement
        obstacle_rect_list = obstacle_movement(obstacle_rect_list)

        # Collision
        game_active = collisions(player_rect, obstacle_rect_list)

    else:
        screen.fill((94, 129, 162))
        screen.blit(player_stand, player_stand_rect)
        obstacle_rect_list.clear()
        player_rect.midbottom = (80, 300)

        score_message = test_font.render(f'Score: {score}', False, (111, 196, 169))
        score_message_rect = score_message.get_rect(center=(400, 360))
        screen.blit(title_surface, title_rect)

        if score == 0:
            screen.blit(game_message, game_message_rect)
        else:
            screen.blit(game_over_message, game_over_rect)
            screen.blit(score_message, score_message_rect)

    # Update the display and maintain frame rate
    pygame.display.update()
    clock.tick(60)
