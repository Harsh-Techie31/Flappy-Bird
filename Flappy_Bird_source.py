import pygame
import random
import sys
import os

a = os.listdir()
print(a)
pygame.mixer.pre_init(buffer=2048)
pygame.init()
pygame.display.set_caption("FlappyBird by Harsh.")

# Global variables
SCREEN = pygame.display.set_mode((288, 512))
clock = pygame.time.Clock()
game_font = pygame.font.Font('04B_19__.TTF', 35)

bg_surface = pygame.image.load('gallery/background1.png').convert_alpha()

base_surface = pygame.image.load('gallery/base.png').convert_alpha()
base_x_pos = 0

bird_surface = pygame.image.load('gallery/bird.png').convert_alpha()
bird_rect = bird_surface.get_rect(center=(80, 256))

pipe_surface = pygame.image.load('gallery/pipe.png').convert_alpha()
pipe_list = []
SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE, 1000)
pipe_height = [i for i in range(250, 301)]

welcome_surface = pygame.image.load('gallery/page.png').convert_alpha()
face_surface = pygame.image.load('gallery/face1.png').convert_alpha()

wing = pygame.mixer.Sound('audio/wing.wav')
wing.set_volume(0.4)

hit = pygame.mixer.Sound('audio/hit.wav')
hit.set_volume(0.3)

point = pygame.mixer.Sound('audio/point.wav')
point.set_volume(0.5)

dababy = pygame.mixer.Sound('audio/dababy_vibez.mp3')
dababy.set_volume(0.01)

# Game Variables
gravity = 0.20
bird_movement = 0
game_active = True
score = 0
high_score = 0
can_score = True
score_sound_countdown = 100


# Functions

def draw_base():
    SCREEN.blit(base_surface, (base_x_pos, 400))
    SCREEN.blit(base_surface, (base_x_pos + 288, 400))


def create_pipe():
    pipe_height2 = random.choice(pipe_height)
    bottom_new_pipe = pipe_surface.get_rect(midtop=(700, pipe_height2))
    top_new_pipe = pipe_surface.get_rect(midbottom=(700, pipe_height2 - 200))
    return bottom_new_pipe, top_new_pipe


def move_pipe(pipes):
    for pipe in pipes:
        pipe.centerx -= 3
    return pipes


def draw_pipes(pipes):
    for pipe in pipes:
        if pipe.bottom >= 400:
            SCREEN.blit(pipe_surface, pipe)
        else:
            ulta_pipe = pygame.transform.flip(pipe_surface, False, True)
            SCREEN.blit(ulta_pipe, pipe)


def check_collisions(pipes):
    global can_score
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            hit.play()
            return False

    if bird_rect.top <= -100 or bird_rect.bottom >= 400:
        hit.play()

        return False
    return True


def score_display(game_state):
    if game_state == 'main_game':
        score_surface = game_font.render(f"{int(score)}", True, (255, 0, 0))
        score_rect = score_surface.get_rect(midtop=(144, 50))
        SCREEN.blit(score_surface, score_rect)
    if game_state == 'game_over':
        score_surface = game_font.render(f"Score:{int(score)}", True, (255, 0, 0))
        score_rect = score_surface.get_rect(midtop=(144, 50))
        SCREEN.blit(score_surface, score_rect)

        high_score_surface = game_font.render(f"High Score:{int(high_score)}", True, (255, 0, 0))
        high_score_rect = high_score_surface.get_rect(midtop=(144, 450))
        SCREEN.blit(high_score_surface, high_score_rect)


def update_score(new_score, new_high_score):
    if new_score > new_high_score:
        new_high_score = new_score
    return new_high_score


def pipe_score_check():
    global score, can_score
    if pipe_list:
        for pipe in pipe_list:
            if 78 < pipe.centerx < 82 and can_score:
                score += 1
                point.play()
                can_score = False
            if pipe.centerx < -20:
                can_score = True


def welcome():
    welcome_rect = welcome_surface.get_rect(center=(144, 267))
    face_rect = face_surface.get_rect(center=(135, 300))
    SCREEN.blit(welcome_surface, welcome_rect)
    SCREEN.blit(face_surface, face_rect)


if __name__ == '__main__':

    while True:
        # dababy.play()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.KEYDOWN and (
                    event.key == pygame.K_SPACE or event.key == pygame.K_UP) and game_active:
                bird_movement = 0
                bird_movement -= 6.5
                wing.play()
            elif event.type == pygame.KEYDOWN and (
                    event.key == pygame.K_SPACE or event.key == pygame.K_UP) and not game_active:
                game_active = True
                pipe_list.clear()
                bird_movement = 0
                bird_rect.center = (80, 0)
                score = 0
                can_score = True

            elif event.type == SPAWNPIPE:
                pipe_list.extend(create_pipe())


            else :
                welcome()

        SCREEN.blit(bg_surface, (0, 0))

        base_x_pos -= 1
        draw_base()
        if base_x_pos <= -288:
            base_x_pos = 0

        if game_active:
            bird_movement += gravity
            bird_rect.centery += bird_movement
            SCREEN.blit(bird_surface, bird_rect)
            game_active = check_collisions(pipe_list)

            pipe_list = move_pipe(pipe_list)
            draw_pipes(pipe_list)

            pipe_score_check()
            score_display('main_game')

        else:
            welcome()
            high_score = update_score(score, high_score)
            score_display('game_over')

        pygame.display.update()
        clock.tick(120)
