import pygame
from pygame.locals import *
import random
import json
import os

from bird import Bird
from pipe import Pipe
from button import Button
from config import Config
from settings_ui import SettingsUI

pygame.init()
pygame.mixer.init()
clock = pygame.time.Clock()
fps = 60

screen_width = 648
screen_height = 702
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Flappy Bird Pro")

font = pygame.font.SysFont("Bauhaus 93", 60)
small_font = pygame.font.SysFont("Bauhaus 93", 30)
white = (255, 255, 255)

ground_scroll = 0
flying = False
game_over = False
in_settings = False
last_pipe = pygame.time.get_ticks() - 1500
score = 0
high_score = 0
pass_pipe = False

if os.path.exists("high_score.json"):
    try:
        with open("high_score.json", "r") as f:
            high_score = json.load(f).get("high_score", 0)
    except: pass

bg = pygame.image.load("img/bg.png")
ground_img = pygame.image.load("img/ground.png")
button_img = pygame.transform.scale(pygame.image.load("img/restart.png"), (200, 70))

# --- Load the new Settings Gear Image ---
try:
    gear_img = pygame.image.load("img/gear.png")
    gear_img = pygame.transform.scale(gear_img, (50, 50)) # Scale it to fit our 50x50 hitbox
except:
    # Fallback just in case the image is missing
    gear_img = pygame.Surface((50, 50), pygame.SRCALPHA)
    pygame.draw.circle(gear_img, (200, 200, 200), (25, 25), 25)

bg_night = bg.copy()
bg_night.fill((60, 60, 80), special_flags=pygame.BLEND_RGB_SUB)
settings_btn_rect = pygame.Rect(20, 20, 50, 50)

try: score_fx = pygame.mixer.Sound("sfx/point.mp3")
except: score_fx = None

try: hit_fx = pygame.mixer.Sound("sfx/hit.mp3")
except: hit_fx = None

try:
    pygame.mixer.music.load("sfx/music.mp3")
    pygame.mixer.music.set_volume(0.15)
    if Config.music_on: pygame.mixer.music.play(-1)
except: pass

def draw_text(text, font, text_col, x, y):
    screen.blit(font.render(text, True, text_col), (x, y))

def draw_medal(score, x, y):
    if score >= 30:
        color, text = (255, 215, 0), "GOLD MEDAL"
    elif score >= 20:
        color, text = (192, 192, 192), "SILVER MEDAL"
    elif score >= 10:
        color, text = (205, 127, 50), "BRONZE MEDAL"
    else:
        return

    pygame.draw.rect(screen, (200, 40, 40), (x - 15, y - 30, 30, 45))
    pygame.draw.circle(screen, color, (x, y + 15), 25)
    pygame.draw.circle(screen, white, (x, y + 15), 25, 3)
    draw_text(text, small_font, color, x - 75, y + 55)

bird_group = pygame.sprite.Group()
pipe_group = pygame.sprite.Group()
flappy = Bird(100, int(screen_height / 2), 0)
bird_group.add(flappy)
restart_btn = Button(screen_width // 2 - 100, screen_height // 2 - 35, button_img)
settings_menu = SettingsUI(screen, font, small_font)

run = True
while run:
    clock.tick(fps)
    
    current_bg = bg_night if (score // 20) % 2 == 1 else bg
    screen.blit(current_bg, (0, 0))

    if in_settings:
        settings_menu.draw()
        for event in pygame.event.get():
            if event.type == QUIT: run = False
            if event.type == MOUSEBUTTONDOWN: settings_menu.handle_click(event.pos)
            if event.type == KEYDOWN and event.key == K_ESCAPE: in_settings = False
        pygame.display.update()
        continue

    pipe_group.draw(screen)
    bird_group.draw(screen)
    bird_group.update(flying, game_over)
    screen.blit(ground_img, (ground_scroll, 576))

    if not flying and not game_over:
        draw_text("PRESS SPACE TO FLY", small_font, white, 190, 250)
        draw_text(f"BEST SCORE: {high_score}", small_font, white, 230, 300)
        
        # --- Draw the Gear Image instead of shapes ---
        screen.blit(gear_img, (settings_btn_rect.x, settings_btn_rect.y))

    else:
        if not game_over:
            draw_text(str(score), font, white, int(screen_width / 2), 20)
        else:
            if not flying:
                draw_medal(score, int(screen_width / 2), 150)
                if restart_btn.draw(screen):
                    game_over = False
                    flying = False
                    score = 0
                    pipe_group.empty()
                    flappy.rect.center = [100, int(screen_height / 2)]
                    flappy.vel = 0
                    pass_pipe = False
                    last_pipe = pygame.time.get_ticks() - Config.get_pipe_frequency(0)

    if len(pipe_group) > 0:
        if bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.left and \
           bird_group.sprites()[0].rect.right < pipe_group.sprites()[0].rect.right and not pass_pipe:
            pass_pipe = True
        if pass_pipe and bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.right:
            score += 1
            pass_pipe = False
            if Config.sfx_on and score_fx: score_fx.play()

    if pygame.sprite.groupcollide(bird_group, pipe_group, False, False) or flappy.rect.top < 0:
        if not game_over:
            if Config.sfx_on and hit_fx: hit_fx.play()
            if score > high_score:
                high_score = score
                with open("high_score.json", "w") as f: json.dump({"high_score": high_score}, f)
        game_over = True

    if flappy.rect.bottom >= 576:
        if flying: 
            if Config.sfx_on and hit_fx: hit_fx.play()
            flying = False
            
        if not game_over:
            if score > high_score:
                high_score = score
                with open("high_score.json", "w") as f: json.dump({"high_score": high_score}, f)
        game_over = True

    if not game_over and flying:
        current_speed = Config.get_pipe_speed(score)
        current_freq = Config.get_pipe_frequency(score)

        time_now = pygame.time.get_ticks()
        if time_now - last_pipe > current_freq:
            h = random.randint(-100, 100)
            pipe_group.add(Pipe(screen_width, int(screen_height / 2) + h, -1))
            pipe_group.add(Pipe(screen_width, int(screen_height / 2) + h, 1))
            last_pipe = time_now

        ground_scroll -= current_speed
        if abs(ground_scroll) > 35: ground_scroll = 0
        pipe_group.update(current_speed)

    for event in pygame.event.get():
        if event.type == QUIT: run = False
        if event.type == MOUSEBUTTONDOWN and not game_over:
            if not flying:
                if settings_btn_rect.collidepoint(event.pos): in_settings = True
                else: flying = True
            elif flying:
                pass
                
        if event.type == KEYDOWN and not flying and not game_over and event.key in [K_SPACE, K_UP, K_TAB]:
            flying = True

    pygame.display.update()
pygame.quit()