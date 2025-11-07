"""
Спільні UI-компоненти: кнопка, лейбл, панель життя/манти, віджети меню, повідомлення «PAUSE»
"""

import pygame

class Button:
    def __init__(self, rect, text, callback, font, color=(255,255,255)):
        self.rect = pygame.Rect(rect)
        self.text = text
        self.callback = callback
        self.font = font
        self.color = color

    def draw(self, surface):
        pygame.draw.rect(surface, (50,50,50), self.rect)
        text_surf = self.font.render(self.text, True, self.color)
        surface.blit(text_surf, text_surf.get_rect(center=self.rect.center))

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.callback()

class Label:
    def __init__(self, pos, text, font, color=(255,255,255)):
        self.pos = pos
        self.text = text
        self.font = font
        self.color = color

    def draw(self, surface):
        text_surf = self.font.render(self.text, True, self.color)
        surface.blit(text_surf, self.pos)

class HealthBar:
    def __init__(self, pos, size, max_hp):
        self.pos = pos
        self.size = size
        self.max_hp = max_hp
        self.current_hp = max_hp

    def draw(self, surface):
        pygame.draw.rect(surface, (100,0,0), (*self.pos, self.size[0], self.size[1]))
        hp_width = int(self.current_hp / self.max_hp * self.size[0])
        pygame.draw.rect(surface, (0,255,0), (*self.pos, hp_width, self.size[1]))
