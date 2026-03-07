import pygame
from config import Config

class Bird(pygame.sprite.Sprite):
    def __init__(self, x, y, vel):
        pygame.sprite.Sprite.__init__(self)
        self.images = [pygame.image.load(f"img/bird{num}.png") for num in range(1, 4)]
        self.index = 0
        self.counter = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.vel = vel
        self.clicked = False
        
        # Load the jump sound safely
        try:
            self.flap_fx = pygame.mixer.Sound("sfx/wing.mp3")
        except:
            print("Could not load wing.mp3")
            self.flap_fx = None

    def update(self, flying, game_over):
        if flying:
            self.vel += 0.5
            if self.vel > 8: self.vel = 8
            if self.rect.bottom < 576: self.rect.y += int(self.vel)

        if not game_over:
            keys = pygame.key.get_pressed()
            mouse_click = pygame.mouse.get_pressed()[0] == 1
            keyboard_jump = keys[pygame.K_SPACE] or keys[pygame.K_UP] or keys[pygame.K_TAB]
            
            if (mouse_click or keyboard_jump) and not self.clicked:
                self.clicked = True
                self.vel = -10
                
                # Play the wing flap sound
                if Config.sfx_on and self.flap_fx:
                    self.flap_fx.play()

            if not mouse_click and not keyboard_jump:
                self.clicked = False

            self.counter += 1
            if self.counter > 5:
                self.counter = 0
                self.index = (self.index + 1) % len(self.images)
            
            self.image = pygame.transform.rotate(self.images[self.index], self.vel * -2)
        else:
            self.image = pygame.transform.rotate(self.images[self.index], -90)