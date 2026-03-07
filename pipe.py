import pygame
from config import Config

class Pipe(pygame.sprite.Sprite):
    def __init__(self, x, y, position):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("img/pipe.png")
        self.rect = self.image.get_rect()
        
        gap = 160 if Config.hard_mode else 200
        
        if position == 1:
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect.bottomleft = [x, y - int(gap / 2)]
        if position == -1:
            self.rect.topleft = [x, y + int(gap / 2)]

    def update(self, speed):
        self.rect.x -= speed
        if self.rect.right < 0:
            self.kill()