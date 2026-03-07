import pygame
from config import Config

class SettingsMenu:
    def __init__(self, screen, font, small_font):
        self.screen = screen
        self.font = font
        self.small_font = small_font
        
        # Switch dimensions
        self.sw_width = 60
        self.sw_height = 30
        
        # Positions for our three toggles
        self.music_rect = pygame.Rect(400, 285, self.sw_width, self.sw_height)
        self.sfx_rect = pygame.Rect(400, 345, self.sw_width, self.sw_height)
        self.diff_rect = pygame.Rect(400, 405, self.sw_width, self.sw_height)

    def draw_switch(self, rect, is_on):
        # Draw background track
        color = (0, 200, 0) if is_on else (100, 100, 100)
        pygame.draw.rect(self.screen, color, rect, border_radius=15)
        
        # Draw knob
        knob_x = rect.right - 15 if is_on else rect.left + 15
        pygame.draw.circle(self.screen, (255, 255, 255), (knob_x, rect.centery), 12)

    def draw(self):
        overlay = pygame.Surface((648, 702), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 200))
        self.screen.blit(overlay, (0, 0))
        
        pygame.draw.rect(self.screen, (40, 40, 40), (120, 150, 410, 400), border_radius=15)
        self.draw_text("SETTINGS", self.font, (255, 255, 255), 210, 170)
        
        # Labels
        self.draw_text("MUSIC", self.small_font, (255, 255, 255), 180, 280)
        self.draw_text("SFX", self.small_font, (255, 255, 255), 180, 340)
        self.draw_text("HARD MODE", self.small_font, (255, 255, 255), 180, 400)
        
        # Draw the Switches
        self.draw_switch(self.music_rect, Config.music_on)
        self.draw_switch(self.sfx_rect, Config.sfx_on)
        self.draw_switch(self.diff_rect, Config.difficulty == "Hard")
        
        self.draw_text("Click switches to toggle", self.small_font, (150, 150, 150), 190, 480)
        self.draw_text("Press 'S' to Save", self.small_font, (0, 255, 0), 240, 520)

    def draw_text(self, text, font, col, x, y):
        img = font.render(text, True, col)
        self.screen.blit(img, (x, y))

    def handle_mouse(self, pos):
        # Check music toggle
        if self.music_rect.collidepoint(pos):
            Config.music_on = not Config.music_on
            if Config.music_on: pygame.mixer.music.unpause()
            else: pygame.mixer.music.pause()
            
        # Check SFX toggle
        if self.sfx_rect.collidepoint(pos):
            Config.sfx_on = not Config.sfx_on
            
        # Check Difficulty toggle
        if self.diff_rect.collidepoint(pos):
            Config.difficulty = "Hard" if Config.difficulty == "Normal" else "Normal"