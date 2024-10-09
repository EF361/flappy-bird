import pygame
from pygame.locals import *  # noqa: F403
import random

# import self define game modules
from bird import Bird
from pipe import Pipe

pygame.init()

clock = pygame.time.Clock()
fps = 60

screen_width = 648
screen_height = 702

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Flappy Bird")


# define game variables
ground_scroll = 0
scroll_speed = 4
flying = False
game_over = False
pipe_gap = 150
pipe_frequency = 1500  # milliseconds
last_pipe = pygame.time.get_ticks() - pipe_frequency

# load images
bg = pygame.image.load("img/bg.png")
ground_img = pygame.image.load("img/ground.png")


bird_group = pygame.sprite.Group()
pipe_group = pygame.sprite.Group()


flappy = Bird(100, int(screen_height / 2))

bird_group.add(flappy)


run = True
while run:
    clock.tick(fps)

    # draw background
    screen.blit(bg, (0, 0))

    bird_group.draw(screen)
    bird_group.update(flying, game_over)
    pipe_group.draw(screen)

    # draw the ground
    screen.blit(ground_img, (ground_scroll, 576))

    # look for collision
    if (
        pygame.sprite.groupcollide(bird_group, pipe_group, False, False)
        or flappy.rect.top < 0
    ):
        game_over = True

    # check if bird has hit the ground
    if flappy.rect.bottom >= 576:
        game_over = True
        flying = False

    if not game_over and flying:
        # generate new pipes
        time_now = pygame.time.get_ticks()
        if time_now - last_pipe > pipe_frequency:
            pipe_height = random.randint(-100, 100)
            btm_pipe = Pipe(screen_width, int(screen_height / 2) + pipe_height, -1)
            top_pipe = Pipe(screen_width, int(screen_height / 2) + pipe_height, 1)
            pipe_group.add(btm_pipe)
            pipe_group.add(top_pipe)
            last_pipe = time_now

        # draw and scroll the ground
        ground_scroll -= scroll_speed
        if abs(ground_scroll) > 35:
            ground_scroll = 0

        pipe_group.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN and not flying and not game_over:
            flying = True

    pygame.display.update()

pygame.quit()
