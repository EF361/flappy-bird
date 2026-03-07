import pygame
from config import Config

class SettingsUI:
    def __init__(self, screen, font, small_font):
        self.screen = screen
        self.font = font
        self.small_font = small_font
        # Create clickable hitboxes for the switches
        self.switches = {
            "music": pygame.Rect(420, 275, 60, 30),
            "sfx": pygame.Rect(420, 335, 60, 30),
            "diff": pygame.Rect(420, 395, 60, 30)
        }

    def draw_switch(self, rect, is_on):
        # Green if ON, Gray if OFF
        color = (0, 255, 0) if is_on else (150, 150, 150)
        pygame.draw.rect(self.screen, color, rect, border_radius=15)
        # Draw the white circle (knob)
        knob_x = rect.right - 15 if is_on else rect.left + 15
        pygame.draw.circle(self.screen, (255, 255, 255), (knob_x, rect.centery), 12)

    def draw(self):
        # Draw Menu Box
        pygame.draw.rect(self.screen, (40, 40, 40), (120, 150, 410, 350), border_radius=15)
        self.screen.blit(self.font.render("SETTINGS", True, (255, 255, 255)), (210, 170))
        
        # Draw Labels
        self.screen.blit(self.small_font.render("MUSIC", True, (255, 255, 255)), (180, 280))
        self.screen.blit(self.small_font.render("SFX", True, (255, 255, 255)), (180, 340))
        self.screen.blit(self.small_font.render("HARD MODE", True, (255, 255, 255)), (180, 400))
        
        # Draw Switches based on Config
        self.draw_switch(self.switches["music"], Config.music_on)
        self.draw_switch(self.switches["sfx"], Config.sfx_on)
        self.draw_switch(self.switches["diff"], Config.hard_mode)
        
        self.screen.blit(self.small_font.render("Press ESC to Close", True, (0, 255, 0)), (200, 460))

    def handle_click(self, pos):
        # Check which switch was clicked with the mouse
        if self.switches["music"].collidepoint(pos):
            Config.music_on = not Config.music_on
            if Config.music_on: pygame.mixer.music.unpause()
            else: pygame.mixer.music.pause()
        elif self.switches["sfx"].collidepoint(pos):
            Config.sfx_on = not Config.sfx_on
        elif self.switches["diff"].collidepoint(pos):
            Config.hard_mode = not Config.hard_mode