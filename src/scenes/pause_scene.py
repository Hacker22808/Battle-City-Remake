"""
Оверлей з варіантами «Продовжити», «Вийти в меню». Повертає керування в game_scene або робить перехід у menu_scene.
"""

import pygame
from scenes.menu_scene import Button

class PauseScene:
    def __init__(self, scene_manager, settings):
        self.scene_manager = scene_manager
        self.settings = settings
        self.screen = pygame.display.get_surface()
        
        # Шрифти
        self.title_font = pygame.font.Font(None, 48)
        self.button_font = pygame.font.Font(None, 36)
        
        # Кнопки
        w, h = self.screen.get_size()
        button_width, button_height = 250, 50
        center_x = w // 2 - button_width // 2
        center_y = h // 2
        
        self.buttons = [
            Button("Продовжити", (center_x, center_y - 40, button_width, button_height), 
                  lambda: self.scene_manager.change("game")),
            Button("Вийти в меню", (center_x, center_y + 40, button_width, button_height), 
                  lambda: self.scene_manager.change("menu"))
        ]

    def handle_event(self, event):
        """Обробка подій"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.scene_manager.change("game")
                
        for button in self.buttons:
            button.handle_event(event)

    def update(self, dt):
        """Оновлення сцени"""
        if self.current_scene:
            self.current_scene.update(dt)

    def draw(self, screen):
        """Відображення паузи"""
        # Напівпрозорий оверлей
        overlay = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        screen.blit(overlay, (0, 0))
        
        # Заголовок
        title_text = self.title_font.render("ПАУЗА", True, (255, 255, 255))
        title_rect = title_text.get_rect(center=(screen.get_width()//2, screen.get_height()//2 - 100))
        screen.blit(title_text, title_rect)
        
        # Кнопки
        for button in self.buttons:
            button.draw(screen, self.button_font)
        
        # Підказка
        hint_font = pygame.font.Font(None, 24)
        hint_text = hint_font.render("ESC - продовжити гру", True, (200, 200, 200))
        screen.blit(hint_text, (screen.get_width()//2 - hint_text.get_width()//2, 
                              screen.get_height()//2 + 120))