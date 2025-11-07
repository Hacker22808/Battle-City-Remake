"""
Основна сцена рівня: ініціалізує рівень (через systems/level_system.py), створює сутності (гравець, вороги, базу), реєструє системи (колізії, стрільба, AI). Обробляє паузу/перехід рівня/програш.
"""


import pygame
from enum import Enum

class GameState(Enum):
    RUNNING = 1
    PAUSED = 2
    LEVEL_COMPLETE = 3
    GAME_OVER = 4

class GameScene:
    def __init__(self, scene_manager, settings):
        self.scene_manager = scene_manager
        self.settings = settings
        self.screen = pygame.display.get_surface()
        self.state = GameState.RUNNING
        
        # Ініціалізація систем
        self.level_system = None
        self.collision_system = None
        self.shooting_system = None
        self.ai_system = None
        
        # Сутності гри
        self.player = None
        self.enemies = []
        self.base = None
        self.bullets = []
        self.blocks = []
        
        # UI
        self.font = pygame.font.Font(None, 36)
        
        # Завантаження рівня
        self.current_level = 1
        self.load_level(self.current_level)

    def load_level(self, level):
        """Завантаження рівня"""
        # Тимчасові заглушки для демонстрації
        screen_width, screen_height = self.screen.get_size()
        
        # Створення гравця
        self.player = type('Player', (), {})()
        self.player.rect = pygame.Rect(screen_width//2 - 20, screen_height - 100, 40, 40)
        self.player.health = 100
        
        # Створення бази
        self.base = type('Base', (), {})()
        self.base.rect = pygame.Rect(screen_width//2 - 30, screen_height - 80, 60, 60)
        self.base.health = 200
        
        # Створення ворогів
        self.enemies = []
        for i in range(3):
            enemy = type('Enemy', (), {})()
            enemy.rect = pygame.Rect(100 + i * 150, 100, 35, 35)
            enemy.health = 50
            self.enemies.append(enemy)
        
        self.bullets = []

    def handle_event(self, event):
        """Обробка подій"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.scene_manager.change("pause")
            elif event.key == pygame.K_p:
                self.toggle_pause()

    def toggle_pause(self):
        """Перемикач паузи"""
        if self.state == GameState.RUNNING:
            self.state = GameState.PAUSED
        elif self.state == GameState.PAUSED:
            self.state = GameState.RUNNING

    def update(self, dt):
        """Оновлення стану гри"""
        if self.state != GameState.RUNNING:
            return
            
        # Тимчасова логіка оновлення для демонстрації
        keys = pygame.key.get_pressed()
        speed = 200 * dt
        
        if keys[pygame.K_a]:
            self.player.rect.x -= speed
        if keys[pygame.K_d]:
            self.player.rect.x += speed
        if keys[pygame.K_w]:
            self.player.rect.y -= speed
        if keys[pygame.K_s]:
            self.player.rect.y += speed
            
        # Обмеження руху в межах екрану
        self.player.rect.clamp_ip(self.screen.get_rect())

    def draw(self, screen):
        """Відображення гри"""
        # Фон
        screen.fill((20, 20, 30))
        
        # Малювання об'єктів
        pygame.draw.rect(screen, (0, 100, 200), self.player.rect)  # Гравець
        pygame.draw.rect(screen, (100, 100, 100), self.base.rect)  # База
        
        for enemy in self.enemies:
            pygame.draw.rect(screen, (200, 50, 50), enemy.rect)  # Вороги
        
        # UI
        health_text = self.font.render(f"HP: {self.player.health}", True, (255, 255, 255))
        screen.blit(health_text, (10, 10))
        
        level_text = self.font.render(f"Рівень: {self.current_level}", True, (255, 255, 255))
        screen.blit(level_text, (10, 50))
        
        # Екран паузи
        if self.state == GameState.PAUSED:
            overlay = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 180))
            screen.blit(overlay, (0, 0))
            
            pause_text = self.font.render("ПАУЗА", True, (255, 255, 255))
            screen.blit(pause_text, (screen.get_width()//2 - pause_text.get_width()//2, 
                                   screen.get_height()//2))