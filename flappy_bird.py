import pygame

pygame.init()
screen_width = 500
screen_height = 650

# set the screen size and title
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Flappy Bird")

# load images
bg = pygame.image.load("img/bg.png")

run = True
while run:
    # show images
    screen.blit(bg, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()

pygame.quit()
