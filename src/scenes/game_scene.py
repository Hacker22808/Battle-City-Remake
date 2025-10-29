"""
Основна сцена рівня: ініціалізує рівень (через systems/level_system.py), створює сутності (гравець, вороги, базу), реєструє системи (колізії, стрільба, AI). Обробляє паузу/перехід рівня/програш.
"""

import pygame
from ..core.scene import Scene
from ..core import constants as C
from ..systems.level_system import LevelSystem
from ..systems.collision_system import CollisionSystem
from ..systems.shooting_system import ShootingSystem
from ..systems.ai_system import AISystem
from .pause_scene import PauseScene

class GameScene(Scene):
    def enter(self, **kwargs):
        self.level = LevelSystem(self.app.assets)
        self.player, self.enemies, self.blocks, self.eagle = self.level.build()
        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.bullets = pygame.sprite.Group()

        for b in self.blocks: self.all_sprites.add(b, layer=b.layer)
        for e in self.enemies: self.all_sprites.add(e, layer=e.layer)
        if self.eagle: self.all_sprites.add(self.eagle, layer=self.eagle.layer)
        self.all_sprites.add(self.player, layer=self.player.layer)

        self.collision = CollisionSystem(self.app.physics)
        self.shooting = ShootingSystem(self.app.assets)
        self.ai = AISystem(self.app.physics)

    def handle_events(self, events):
        for e in events:
            if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
                self.app.change_scene(PauseScene, prev_scene=self)

    def update(self):
        dt = self.app.time.dt
        # рух гравця
        v = self.player.handle_input(self.app.input)
        dx, dy = int(v.x * self.player.speed * dt), int(v.y * self.player.speed * dt)
        self.app.physics.move_and_collide(self.player, dx, dy, self.blocks)

        # постріл
        if self.app.input.pressed("fire"):
            self.shooting.player_try_shoot(self.player, self.bullets)

        # AI
        self.ai.update(dt, self.enemies, self.blocks)
        for e in self.enemies:
            self.shooting.enemy_try_shoot(e, self.bullets)

        # update куль і колізії
        for b in list(self.bullets): b.update(dt)
        self.collision.update(self.player, self.enemies, self.bullets, self.blocks, self.eagle, self._on_event)

        self.all_sprites.update(dt)

    def _on_event(self, name):
        if name == "eagle_down":
            # простий рестарт рівня
            self.enter()

    def render(self, screen):
        self.all_sprites.draw(screen)
        for b in self.bullets:
            screen.blit(b.image, b.rect)
