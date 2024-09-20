import pygame
from bird import Bird

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
    screen.blit(bg, (0, 0))

    bird_group.draw(screen)
    bird_group.update(flying, game_over)

    # draw the ground
    screen.blit(ground_img, (ground_scroll, 576))

    # check if bird has hit the ground
    if flappy.rect.bottom > 576:
        game_over = True
        flying = False

    if not game_over:
        # draw and scroll the ground
        ground_scroll -= scroll_speed
        if abs(ground_scroll) > 35:
            ground_scroll = 0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN and not flying and not game_over:
            flying = True

    pygame.display.update()

pygame.quit()
