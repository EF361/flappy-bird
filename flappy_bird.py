import pygame
from bird import Bird

pygame.init()

clock = pygame.time.Clock()
fps = 60


screen_width = 648
screen_height = 702

# set the screen size and title
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Flappy Bird")

# define game variables
ground_scroll = 0
scroll_speed = 4

# load images
bg = pygame.image.load("img/bg.png")
ground_img = pygame.image.load("img/ground.png")

bird_group = pygame.sprite.Group()
flappy = Bird(100, int(screen_height / 2))
bird_group.add(flappy)

run = True
while run:
    clock.tick(fps)

    # draw background
    screen.blit(bg, (0, -100))

    bird_group.draw(screen)
    bird_group.update()

    # draw and scroll the ground
    screen.blit(ground_img, (ground_scroll, 576))
    ground_scroll -= scroll_speed
    if abs(ground_scroll) > 35:
        ground_scroll = 0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()

pygame.quit()
