import pygame
import random
import math
import time
from pygame import mixer

class Base(pygame.sprite.Sprite):
    """Главная база игрока (Eagle Base). Потеря = поражение."""

    def __init__(self, pos):
        super().__init__()
        self.image = pygame.Surface((64, 64), pygame.SRCALPHA)
        self.rect = self.image.get_rect(center=pos)

        # === Статистика базы ===
        self.max_hp = 100
        self.hp = self.max_hp
        self.armor = 20  # броня снижает урон
        self.alive = True
        self.flash_time = 0
        self.hit_timer = 0

        # === Эффекты ===
        self.last_damage_time = 0
        self.damage_flash_duration = 0.2

        # === Визуал ===
        self.base_color = (240, 200, 40)
        self.update_image()

        # === Аудио ===
        try:
            mixer.init()
            self.explosion_sound = mixer.Sound("assets/explosion.wav")
            self.hit_sound = mixer.Sound("assets/hit.wav")
        except Exception:
            self.explosion_sound = None
            self.hit_sound = None

        # === Частицы взрыва ===
        self.particles = []

    # ----------------------------------------------------------------
    def update_image(self):
        """Перерисовывает базу с учетом HP."""
        self.image.fill((0, 0, 0, 0))  # очистка

        # фон — щит
        pygame.draw.rect(self.image, (50, 50, 50), self.rect.inflate(-2, -2))

        # цвет меняется от жёлтого к красному
        ratio = self.hp / self.max_hp
        color = (
            int(255 * (1 - ratio) + self.base_color[0] * ratio),
            int(self.base_color[1] * ratio),
            int(self.base_color[2] * ratio),
        )
        pygame.draw.circle(self.image, color, (32, 32), 28)

        # индикатор здоровья
        bar_w = int(60 * ratio)
        pygame.draw.rect(self.image, (0, 255, 0), (2, 56, bar_w, 6))
        pygame.draw.rect(self.image, (0, 0, 0), (2, 56, 60, 6), 1)

        # эффект "мигания" при получении урона
        if time.time() - self.last_damage_time < self.damage_flash_duration:
            flash = pygame.Surface((64, 64), pygame.SRCALPHA)
            flash.fill((255, 50, 50, 100))
            self.image.blit(flash, (0, 0))

    # ----------------------------------------------------------------
    def take_damage(self, amount):
        """Получить урон с учетом брони."""
        if not self.alive:
            return

        # применяем броню
        reduced = max(0, amount - self.armor / 2)
        self.hp -= reduced
        self.last_damage_time = time.time()

        if self.hit_sound:
            self.hit_sound.play()

        if self.hp <= 0:
            self.destroy()
        else:
            self.update_image()

    # ----------------------------------------------------------------
    def repair(self, amount):
        """Восстановить здоровье."""
        if self.alive:
            self.hp = min(self.max_hp, self.hp + amount)
            self.update_image()

    # ----------------------------------------------------------------
    def destroy(self):
        """Взрыв и уничтожение базы."""
        if not self.alive:
            return
        self.alive = False
        if self.explosion_sound:
            self.explosion_sound.play()
        self.spawn_explosion_particles()

    # ----------------------------------------------------------------
    def spawn_explosion_particles(self):
        """Создать частицы при уничтожении."""
        for _ in range(30):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(80, 250)
            vel = (math.cos(angle) * speed, math.sin(angle) * speed)
            color = random.choice([(255, 120, 0), (255, 255, 0), (200, 80, 20)])
            self.particles.append([pygame.Vector2(self.rect.center), vel, color, 2.5])

    # ----------------------------------------------------------------
    def update_particles(self, dt):
        """Анимация частиц взрыва."""
        new_particles = []
        for p in self.particles:
            pos, vel, color, life = p
            pos.x += vel[0] * dt
            pos.y += vel[1] * dt
            life -= dt
            if life > 0:
                new_particles.append([pos, vel, color, life])
        self.particles = new_particles

    # ----------------------------------------------------------------
    def draw(self, surface):
        """Отрисовка базы и частиц."""
        surface.blit(self.image, self.rect)
        for pos, _, color, life in self.particles:
            alpha = int(255 * (life / 2.5))
            pygame.draw.circle(surface, color, (int(pos.x), int(pos.y)), 3)
            overlay = pygame.Surface((6, 6), pygame.SRCALPHA)
            overlay.fill((*color, alpha))
            surface.blit(overlay, (pos.x - 3, pos.y - 3))
