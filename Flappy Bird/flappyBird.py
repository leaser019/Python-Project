
import pygame
import sys
import random


def draw_floor():
    screen.blit(floor_backGround,
                (floor_backGround_x_pos, floor_backGround_y_pos))
    screen.blit(floor_backGround, (floor_backGround_x_pos +
                width_screen, floor_backGround_y_pos))


def create_pipe():
    pipe_height = [300, 400, 500]
    pipe_x_pos = 500
    pipe_y_pos = random.choice(pipe_height)
    pipe_rect_bottom = pipe_img.get_rect(midtop=(pipe_x_pos, pipe_y_pos))
    pipe_y_pos -= 200
    pipe_rect_top = pipe_img.get_rect(midbottom=(pipe_x_pos, pipe_y_pos))
    return pipe_rect_bottom, pipe_rect_top


def display_score(game_state):
    if game_state == "main_game":
        score_display = game_font.render(
            str(int(score)), True, (255, 255, 255))
        score_rect = score_display.get_rect(center=(width_screen/2, 100))
        screen.blit(score_display, score_rect)
    if game_state == "game_over":
        score_display = highest_score_font.render(
            f"Score: {(int(score))}", True, (255, 255, 255))
        score_rect = score_display.get_rect(center=(width_screen/2, 300))
        screen.blit(score_display, score_rect)
        highest_score_display = highest_score_font.render(
            f"Highest Score: {(int(highest_score))}", True, (255, 255, 255))
        highest_score_rect = highest_score_display.get_rect(
            center=(width_screen/2, 100))
        screen.blit(highest_score_display, highest_score_rect)


def move_pipe(pipes):
    for pipe in pipes:
        pipe.centerx -= 2
    return pipes


def draw_pipe(pipes):
    for pipe in pipes:
        if pipe.bottom >= height_screen:
            screen.blit(pipe_img, pipe)
        else:
            flip_pipe = pygame.transform.flip(pipe_img, False, True)
            screen.blit(flip_pipe, pipe)


def check_collision(pipes):
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            hit_sound.play()
            return False
        if bird_rect.top <= -20 or bird_rect.bottom >= floor_backGround_y_pos + 40:
            hit_sound.play()
            return False
    return True


def rotate_bird(main_bird):
    temp_bird = pygame.transform.rotozoom(main_bird, -bird_movement*5, 1)
    return temp_bird


def check_score(pipes):
    score_temp = score
    for pipe in pipes:
        if bird_rect.centerx == pipe.centerx:
            score_temp += 0.5
        if score_temp > score:
            add_point_sound.play()
    return score_temp




pygame.init()
pygame.mixer.pre_init(frequency=44100, size=-16, channels=2, buffer=512)
pygame.display.set_caption("Flappy Bird")
pygame.display.set_icon(pygame.transform.scale2x(pygame.image.load("./assets/img/icon.ico")))
# Initial for game
width_screen = 432
height_screen = 768
gravity = 0.1
bird_movement = 0
game_active = False
score = 0
highest_score = 0
time_make_pipe = 1600
time_flag_swing = 90
floor_backGround_x_pos = 0
floor_backGround_y_pos = 600
floor_backGround_x_pos_change = 2

screen = pygame.display.set_mode((width_screen, height_screen))
game_start_display = pygame.transform.scale2x(
    pygame.image.load("./assets/img/message.png")).convert_alpha()
game_over_display = pygame.transform.scale2x(
    pygame.image.load("./assets\img\gameover.png")).convert_alpha()
clock = pygame.time.Clock()
game_font = pygame.font.Font("./assets/font/04B_19.TTF", 60)
highest_score_font = pygame.font.Font("./assets/font/04B_19.TTF", 40)

# Init and Load Background
backGround = pygame.transform.scale2x(pygame.image.load(
    "./assets/img/background-night.png").convert())

# Init and Load Floor
floor_backGround = pygame.transform.scale2x(
    pygame.image.load("./assets/img/floor.png").convert())

# Init and Load Bird
bird_mid = pygame.transform.scale2x(pygame.image.load(
    "./assets/img/yellowbird-midflap.png").convert_alpha())
bird_upflap = pygame.transform.scale2x(pygame.image.load(
    "./assets/img/yellowbird-upflap.png").convert_alpha())
bird_downflap = pygame.transform.scale2x(pygame.image.load(
    "./assets/img/yellowbird-downflap.png").convert_alpha())
list_bird = [bird_downflap, bird_mid, bird_upflap]
bird_index = 1
bird = list_bird[bird_index]
bird_rect = bird.get_rect(center=(100, height_screen/2))

# Init and Load Pipe
pipe_img = pygame.transform.scale2x(
    pygame.image.load("./assets/img/pipe-green.png").convert_alpha())
list_pipe = []

# Set Timer For PIPE
spawn_pipe = pygame.USEREVENT
pygame.time.set_timer(spawn_pipe, time_make_pipe)

# Set Timer For BIRD
fly = pygame.USEREVENT + 1
pygame.time.set_timer(fly, time_flag_swing)

# Add Sound
flap_sound = pygame.mixer.Sound("./assets/sound/sfx_wing.wav")
add_point_sound = pygame.mixer.Sound("./assets/sound/sfx_point.wav")
hit_sound = pygame.mixer.Sound("./assets/sound/sfx_hit.wav")
die_sound = pygame.mixer.Sound("./assets/sound/sfx_die.wav")
theme_song = pygame.mixer.Sound("./assets/sound/Flappy Bird Theme Song.mp3")

while True:
    # Event
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            # Space to turn up and restart
            if event.key == pygame.K_SPACE and game_active:
                bird_movement = 0
                bird_movement -= gravity*50
                flap_sound.play()
            if event.key == pygame.K_SPACE and game_active == False:
                game_active = True
                list_pipe.clear()
                bird_rect = bird.get_rect(center=(100, height_screen/2))
                bird_movement = 0
                score = 0

        # Bird Flying
        if event.type == fly:
            if (bird_index <= 0 and bird_index < 3):
                bird_index += 1
            else:
                bird_index = 0
        # Make pipe
        if event.type == spawn_pipe:
            list_pipe.extend(create_pipe())
    # Check collision

    # Draw background
    screen.blit(backGround, (0, 0))
    if game_active:
        game_active = check_collision(list_pipe)
        # Draw bird
        bird = list_bird[bird_index]
        rotated_bird = rotate_bird(bird)
        screen.blit(rotated_bird, bird_rect)
        bird_movement += gravity
        bird_rect.centery += bird_movement

        # Draw pipe
        list_pipe = move_pipe(list_pipe)
        draw_pipe(list_pipe)
        score = check_score(list_pipe)
        display_score("main_game")
        if highest_score < score:
            highest_score = score

    else:
        display_score("game_over")
        screen.blit(game_start_display, (60, 180))

    # Draw floor
    draw_floor()
    floor_backGround_x_pos -= floor_backGround_x_pos_change
    if floor_backGround_x_pos <= - width_screen:
        floor_backGround_x_pos = 0

    pygame.display.update()
    clock.tick(120)
