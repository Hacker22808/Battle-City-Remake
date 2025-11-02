import pygame
import math
import random
from bullet import Bullet


class Tank(pygame.sprite.Sprite):
    """
    Клас гравця (танка):
    - рух у 4 сторони
    - стрільба
    - HP, броня, щит
    - анімація гусениць, ефекти пошкодження
    """

    def __init__(self, pos):
        super().__init__()
        self.image = pygame.Surface((40, 40), pygame.SRCALPHA)
        self.rect = self.image.get_rect(center=pos)
        self.color = (100, 200, 100)

        # Бойові параметри
        self.max_hp = 120
        self.hp = self.max_hp
        self.armor = 20
        self.speed = 180
        self.damage = 25
        self.direction = pygame.Vector2(0, -1)
        self.cooldown = 0.0
        self.fire_rate = 0.5
        self.shield_timer = 0.0
        self.damage_boost = 1.0

        # Ефекти
        self.flash_timer = 0
        self.smoke_timer = 0
        self.tracks_phase = 0
        self._draw_tank()

        # Стани
        self.alive = True
        self.exploding = False
        self.explosion_timer = 0

    # ============================================================
    # Малювання
    def _draw_tank(self, damaged=False):
        """Малює тіло танка."""
        surf = self.image
        surf.fill((0, 0, 0, 0))
        body_color = (100, 200, 100) if not damaged else (200, 120, 80)
        pygame.draw.rect(surf, body_color, (4, 4, 32, 32), border_radius=8)
        pygame.draw.rect(surf, (40, 80, 40), (4, 4, 32, 32), 2)

        # башта
        pygame.draw.circle(surf, (20, 40, 20), (20, 20), 8)
        # ствол
        pygame.draw.rect(surf, (60, 120, 60), (18, 0, 4, 12))
        # гусениці
        for i in range(0, 36, 8):
            pygame.draw.line(surf, (60, 60, 60), (6, i + 2), (6, i + 6), 2)
            pygame.draw.line(surf, (60, 60, 60), (34, i + 2), (34, i + 6), 2)

    # ============================================================
    def handle_input(self, keys, dt):
        """Рух і керування танком."""
        if not self.alive:
            return

        vx, vy = 0, 0
        if keys[pygame.K_w]:
            vy -= 1
            self.direction = pygame.Vector2(0, -1)
        elif keys[pygame.K_s]:
            vy += 1
            self.direction = pygame.Vector2(0, 1)
        if keys[pygame.K_a]:
            vx -= 1
            self.direction = pygame.Vector2(-1, 0)
        elif keys[pygame.K_d]:
            vx += 1
            self.direction = pygame.Vector2(1, 0)

        move = pygame.Vector2(vx, vy)
        if move.length_squared() > 0:
            move = move.normalize()
            self.rect.x += move.x * self.speed * dt
            self.rect.y += move.y * self.speed * dt
            self.tracks_phase += dt * 12
            if int(self.tracks_phase * 2) % 2 == 0:
                self.image.fill((10, 10, 10, 30), special_flags=pygame.BLEND_RGBA_SUB)

    # ============================================================
    def shoot(self, bullets_group):
        """Стрільба."""
        if not self.alive or self.cooldown > 0:
            return

        bx = self.rect.centerx + self.direction.x * 24
        by = self.rect.centery + self.direction.y * 24
        bullet = Bullet(
            (bx, by),
            self.direction,
            speed=400,
            damage=self.damage * self.damage_boost,
            color=(255, 255, 120)
        )
        bullets_group.add(bullet)
        self.cooldown = self.fire_rate
        print("🔫 Постріл!")

    # ============================================================
    def take_damage(self, amount):
        """Отримання шкоди з урахуванням броні та щита."""
        if not self.alive:
            return

        if self.shield_timer > 0:
            print("🛡️ Щит поглинув удар!")
            return

        reduced = max(0, amount - self.armor)
        self.hp -= reduced
        self.flash_timer = 0.2
        print(f"💢 Танку завдано {reduced} шкоди. HP: {self.hp}/{self.max_hp}")

        if self.hp <= 0:
            self.destroy()

    # ============================================================
    def destroy(self):
        """Знищення танка."""
        if self.exploding:
            return
        self.alive = False
        self.exploding = True
        self.explosion_timer = 1.2
        print("💥 Танка знищено!")

    # ============================================================
    def heal(self, value):
        """Відновлення HP."""
        self.hp = min(self.max_hp, self.hp + value)
        print(f"💖 HP відновлено до {self.hp}")

    # ============================================================
    def apply_powerup(self, powerup):
        """Застосовує бонус."""
        powerup.apply(self)

    # ============================================================
    def update(self, dt, bullets_group):
        """Оновлення ефектів, таймерів, вибуху."""
        if self.cooldown > 0:
            self.cooldown -= dt
        if self.shield_timer > 0:
            self.shield_timer -= dt
        if self.flash_timer > 0:
            self.flash_timer -= dt
            if int(self.flash_timer * 20) % 2 == 0:
                self.image.fill((255, 255, 255, 80), special_flags=pygame.BLEND_RGBA_ADD)

        if not self.alive:
            self._explode(dt)

        # ефект диму при низькому HP
        if self.hp < self.max_hp * 0.5 and random.random() < 0.03:
            self._emit_smoke()

    # ============================================================
    def _emit_smoke(self):
        """Створює візуальний дим при пошкодженні."""
        surf = pygame.display.get_surface()
        smoke = pygame.Surface((20, 20), pygame.SRCALPHA)
        c = random.randint(150, 200)
        pygame.draw.circle(smoke, (c, c, c, 120), (10, 10), random.randint(5, 9))
        surf.blit(smoke, (self.rect.x + random.randint(0, 20), self.rect.y - 10))

    # ============================================================
    def _explode(self, dt):
        """Анімація вибуху."""
        self.explosion_timer -= dt
        radius = int((1.2 - self.explosion_timer) * 40)
        if radius < 60:
            boom = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
            pygame.draw.circle(
                boom,
                (255, random.randint(100, 200), 0, 160),
                (radius, radius),
                radius
            )
            boom_rect = boom.get_rect(center=self.rect.center)
            pygame.display.get_surface().blit(boom, boom_rect)
        if self.explosion_timer <= 0:
            self.kill()

    # ============================================================
    def draw(self, surface):
        """Малює танк і ефекти."""
        surface.blit(self.image, self.rect)

        # Щит
        if self.shield_timer > 0:
            phase = math.sin(pygame.time.get_ticks() * 0.01) * 50 + 205
            pygame.draw.circle(surface, (phase, phase, 255),
                               self.rect.center, 28, 2)

        # HP bar
        if self.alive:
            hp_ratio = self.hp / self.max_hp
            bar_w = 36
            pygame.draw.rect(surface, (60, 60, 60),
                             (self.rect.x + 2, self.rect.y - 8, bar_w, 5))
            pygame.draw.rect(surface, (100, 255, 100),
                             (self.rect.x + 2, self.rect.y - 8, int(bar_w * hp_ratio), 5))
