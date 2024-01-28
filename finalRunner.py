# Import necessary libraries
import pygame
from sys import exit
from random import randint, choice


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        player_walk_1 = pygame.image.load('data/graphics/FinalFantasy/wol-war1.png').convert_alpha()
        player_walk_2 = pygame.image.load('data/graphics/FinalFantasy/wol-war2.png').convert_alpha()
        self.player_walk = [player_walk_1, player_walk_2]
        self.player_index = 0
        self.player_jump = pygame.image.load('data/graphics/FinalFantasy/wol-war-jump.png').convert_alpha()

        self.image = self.player_walk[self.player_index]
        self.rect = self.image.get_rect(midbottom=(80, 300))
        self.gravity = 0

        self.jump_sound = pygame.mixer.Sound('data/audio/jump.mp3')
        self.jump_sound.set_volume(0.1)

    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >= 300:
            self.gravity = -20
            self.jump_sound.play()

    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= 300:
            self.rect.bottom = 300

    def animation_state(self):
        if self.rect.bottom < 300:
            self.image = self.player_jump
        else:
            self.player_index += 0.1
            if self.player_index >= len(self.player_walk):
                self.player_index = 0
            self.image = self.player_walk[int(self.player_index)]

    def update(self):
        self.player_input()
        self.apply_gravity()
        self.animation_state()


class Obstacle(pygame.sprite.Sprite):
    def __init__(self, type):
        super().__init__()

        if type == 'bat':
            bat_1 = pygame.image.load('data/graphics/FinalFantasy/bat1.png').convert_alpha()
            bat_2 = pygame.image.load('data/graphics/FinalFantasy/bat2.png').convert_alpha()
            self.frames = [bat_1, bat_2]
            y_pos = 190
        else:
            golem_1 = pygame.image.load('data/graphics/FinalFantasy/golem1.png').convert_alpha()
            golem_2 = pygame.image.load('data/graphics/FinalFantasy/golem2.png').convert_alpha()
            self.frames = [golem_1, golem_2]
            y_pos = 300

        self.animation_index = 0
        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect(midbottom=(randint(900, 1100), y_pos))

    def animation_state(self):
        self.animation_index += 0.1
        if self.animation_index >= len(self.frames):
            self.animation_index = 0
        self.image = self.frames[int(self.animation_index)]

    def update(self):
        self.animation_state()
        self.rect.x -= 6
        self.destroy()

    def destroy(self):
        if self.rect.x <= -100:
            self.kill()


def display_score():
    current_time = int(pygame.time.get_ticks() / 1000) - start_time
    score_surface = test_font.render(f'EXP: {current_time}', False, (64, 64, 64))
    score_rect = score_surface.get_rect(center=(400, 50))
    screen.blit(score_surface, score_rect)
    return current_time


def obstacle_movement(obstacle_list):
    if obstacle_list:
        for obstacle_rect in obstacle_list:
            obstacle_rect.x -= 5

            if obstacle_rect.bottom == 300:
                screen.blit(golem_surface, obstacle_rect)
            else:
                screen.blit(bat_surface, obstacle_rect)

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


def collision_sprite():
    if pygame.sprite.spritecollide(player.sprite, obstacle_group, False):
        obstacle_group.empty()
        return False
    else:
        return True


def player_animation():
    global player_surface, player_index

    if player_rect.bottom < 300:
        player_surface = player_jump
    else:
        player_index += 0.1
        if player_index >= len(player_walk):
            player_index = 0
        player_surface = player_walk[int(player_index)]


def crystal_animation():
    global crystal_surfaces, crystal_index  # Use the renamed list variable

    crystal_index += 0.1
    if crystal_index >= len(crystal_surfaces):
        crystal_index = 0
    current_surface = crystal_surfaces[int(crystal_index)]
    return current_surface



# Initialise Pygame
pygame.init()

icon = pygame.image.load('data/graphics/FinalFantasy/final_runner_icon.png')
pygame.display.set_icon(icon)

# Set up the display window
screen = pygame.display.set_mode((800, 400))
pygame.display.set_caption('Final Runner')
clock = pygame.time.Clock()
game_active = False
start_time = 0
score = 0

music_playing = True
bg_music = pygame.mixer.Sound('data/audio/ffxvi-away-8-bit.mp3')
bg_music.play(-1)
bg_music.set_volume(0.3)

# Groups
player = pygame.sprite.GroupSingle()
player.add(Player())

obstacle_group = pygame.sprite.Group()


# Load font for text rendering
test_font = pygame.font.Font('data/font/Pixeltype.ttf', 50)

background_intro_surface = pygame.image.load('data/graphics/background_forest.png').convert()

# Load background images and convert them for optimal performance
background_surface = pygame.image.load('data/graphics/background_cornelia.png').convert()
# ground_surface = pygame.image.load('data/graphics/ground.png').convert()

# Obstacles
# Golem
golem_frame_1 = pygame.image.load('data/graphics/FinalFantasy/golem1.png').convert_alpha()
golem_frame_2 = pygame.image.load('data/graphics/FinalFantasy/golem2.png').convert_alpha()
golem_frames = [golem_frame_1, golem_frame_2]
golem_frame_index = 0
golem_surface = golem_frames[golem_frame_index]

# Bat
bat_frame_1 = pygame.image.load('data/graphics/FinalFantasy/bat1.png').convert_alpha()
bat_frame_2 = pygame.image.load('data/graphics/FinalFantasy/bat2.png').convert_alpha()
bat_frames = [bat_frame_1, bat_frame_2]
bat_frame_index = 0
bat_surface = bat_frames[bat_frame_index]

obstacle_rect_list = []

# Load player image, enable transparency, and set initial position and gravity
player_walk_1 = pygame.image.load('data/graphics/Player/player_walk_1.png').convert_alpha()
player_walk_2 = pygame.image.load('data/graphics/Player/player_walk_2.png').convert_alpha()
player_walk = [player_walk_1, player_walk_2]
player_index = 0
player_jump = pygame.image.load('data/graphics/Player/jump.png').convert_alpha()

player_surface = player_walk[player_index]
player_rect = player_walk_1.get_rect(midbottom=(80, 300))
player_gravity = 0

# Intro Screen
player_stand = pygame.image.load('data/graphics/FinalFantasy/wol-war-cast1.png').convert_alpha()
player_stand = pygame.transform.rotozoom(player_stand, 0, 2)
player_stand_rect = player_stand.get_rect(center=(400, 200))

crystal_surface_1 = pygame.image.load('data/graphics/FinalFantasy/crystal/crystal1.png').convert_alpha()
crystal_surface_2 = pygame.image.load('data/graphics/FinalFantasy/crystal/crystal2.png').convert_alpha()
crystal_surface_3 = pygame.image.load('data/graphics/FinalFantasy/crystal/crystal3.png').convert_alpha()
crystal_surface_4 = pygame.image.load('data/graphics/FinalFantasy/crystal/crystal4.png').convert_alpha()
crystal_surface_5 = pygame.image.load('data/graphics/FinalFantasy/crystal/crystal5.png').convert_alpha()
crystal_surface_6 = pygame.image.load('data/graphics/FinalFantasy/crystal/crystal6.png').convert_alpha()
crystal_surface_7 = pygame.image.load('data/graphics/FinalFantasy/crystal/crystal7.png').convert_alpha()
crystal_surface_8 = pygame.image.load('data/graphics/FinalFantasy/crystal/crystal8.png').convert_alpha()
crystal_surfaces = [
    crystal_surface_1, crystal_surface_2, crystal_surface_3,
    crystal_surface_4, crystal_surface_5, crystal_surface_6,
    crystal_surface_7, crystal_surface_8
]


crystal_index = 0
crystal_surface = crystal_surfaces[crystal_index]
crystal_rect = crystal_surface_1.get_rect(center=(225, 315))


player_ko = pygame.image.load('data/graphics/FinalFantasy/wol-war-ko.png').convert_alpha()
player_ko = pygame.transform.rotozoom(player_ko, 0, 2)
player_ko_rect = player_ko.get_rect(center=(400, 200))

title_surface = test_font.render('Final Runner', False, (245, 245, 220))
title_rect = title_surface.get_rect(center=(400, 80))

game_message = test_font.render('Press SPACE to run!', False, (245, 245, 220))
game_message_rect = game_message.get_rect(center=(400, 320))

sound_option = test_font.render('F1 - Music On/Off', False, (245, 245, 220))
sound_option_rect = sound_option.get_rect(topleft=(10, 10))

exit_message = test_font.render("F9 - Quit", False, (245, 245, 220))
exit_message_rect = exit_message.get_rect(topleft=(650, 10))

game_over_message = test_font.render(f'GAME OVER!', False, (245, 245, 220))
game_over_rect = game_over_message.get_rect(center=(400, 320))

# Timer
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 1500)

golem_animation_timer = pygame.USEREVENT + 2
pygame.time.set_timer(golem_animation_timer, 500)

bat_animation_timer = pygame.USEREVENT + 3
pygame.time.set_timer(bat_animation_timer, 200)

# Main game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        # Handle function key press for music toggle
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_F1:
                music_playing = not music_playing  # Toggle the music state
                if music_playing:
                    bg_music.play(-1)  # Play music
                else:
                    bg_music.stop()  # Stop music

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_F9:
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

        if game_active:
            if event.type == obstacle_timer:
                obstacle_group.add(Obstacle(choice(['bat', 'bat', 'golem', 'golem', 'golem'])))

            if event.type == golem_animation_timer:
                if golem_frame_index == 0:
                    golem_frame_index = 1
                else:
                    golem_frame_index = 0
                golem_surface = golem_frames[golem_frame_index]

            if event.type == bat_animation_timer:
                if bat_frame_index == 0:
                    bat_frame_index = 1
                else:
                    bat_frame_index = 0
                bat_surface = bat_frames[bat_frame_index]

    if game_active:

        # Draw background images
        screen.blit(background_surface, (0, 0))
        # screen.blit(ground_surface, (0, 300))

        # Draw and position the score text
        # pygame.draw.rect(screen, '#c0e8ec', score_rect)
        # pygame.draw.rect(screen, '#c0e8ec', score_rect, 10)
        # screen.blit(score_surface, score_rect)
        score = display_score()

        player.draw(screen)
        player.update()

        obstacle_group.draw(screen)
        obstacle_group.update()

        # Obstacle movement
        obstacle_rect_list = obstacle_movement(obstacle_rect_list)

        # Collision
        game_active = collision_sprite()

    else:
        screen.blit(background_intro_surface, (0, 0))
        obstacle_rect_list.clear()
        player_rect.midbottom = (80, 300)

        score_message = test_font.render(f'EXP Avoided: {score}', False, (245, 245, 220))
        score_message_rect = score_message.get_rect(center=(400, 360))
        screen.blit(title_surface, title_rect)
        current_crystal_surface = crystal_animation()
        screen.blit(current_crystal_surface, crystal_rect)

        if score == 0:
            screen.blit(player_stand, player_stand_rect)
            screen.blit(game_message, game_message_rect)
            screen.blit(sound_option, sound_option_rect)
            screen.blit(exit_message, exit_message_rect)
        else:
            screen.blit(player_ko, player_ko_rect)
            screen.blit(game_over_message, game_over_rect)
            screen.blit(score_message, score_message_rect)

    # Update the display and maintain frame rate
    pygame.display.update()
    clock.tick(60)
