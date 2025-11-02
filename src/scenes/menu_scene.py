"""
Логіка головного меню: кнопки «Грати», «Налаштування» (мінімально — звук/керування), «Вийти». Переходи на game_scene. Завантаження фону/логотипу з assets.
"""

import pygame
import sys

class Button:
    def __init__(self, text, rect, on_click):
        self.text = text
        self.rect = pygame.Rect(rect)
        self.on_click = on_click
        self.hovered = False
        
    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.hovered = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.hovered and self.on_click:
                self.on_click()
                
    def draw(self, screen, font):
        color = (40, 180, 200) if self.hovered else (30, 140, 160)
        pygame.draw.rect(screen, color, self.rect, border_radius=10)
        pygame.draw.rect(screen, (0, 0, 0), self.rect, width=2, border_radius=10)
        
        text_surf = font.render(self.text, True, (240, 240, 240))
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)

class MenuScene:
    def __init__(self, scene_manager, settings):
        self.scene_manager = scene_manager
        self.settings = settings
        self.screen = pygame.display.get_surface()
        
        # Шрифти
        self.title_font = pygame.font.Font(None, 64)
        self.button_font = pygame.font.Font(None, 36)
        
        # Кнопки
        w, h = self.screen.get_size()
        button_width, button_height = 300, 60
        center_x = w // 2 - button_width // 2
        start_y = h // 2 - 100
        
        self.buttons = [
            Button("Грати", (center_x, start_y, button_width, button_height), 
                  lambda: self.scene_manager.change("game")),
            Button("Налаштування", (center_x, start_y + 80, button_width, button_height), 
                  lambda: print("Settings")),
            Button("Вийти", (center_x, start_y + 160, button_width, button_height), 
                  self.exit_game)
        ]
        
        # Фон
        self.bg_color = (14, 16, 22)

    def exit_game(self):
        """Вихід з гри"""
        pygame.quit()
        sys.exit()

    def handle_event(self, event):
        """Обробка подій"""
        for button in self.buttons:
            button.handle_event(event)

    def update(self, dt):
        """Оновлення сцени"""
        pass

    def draw(self, screen):
        """Відображення меню"""
        # Фон
        screen.fill(self.bg_color)
        
        # Заголовок
        title_text = self.title_font.render("TANK BATTLE", True, (240, 240, 255))
        title_rect = title_text.get_rect(center=(screen.get_width()//2, 150))
        screen.blit(title_text, title_rect)
        
        # Кнопки
        for button in self.buttons:
            button.draw(screen, self.button_font)
        
        # Підказка
        hint_font = pygame.font.Font(None, 24)
        hint_text = hint_font.render("Demo Version - Pygame Tank Game", True, (200, 200, 220))
        screen.blit(hint_text, (10, screen.get_height() - 30))