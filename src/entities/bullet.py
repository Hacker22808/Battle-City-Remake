import pygame
import math
import random

class Bullet(pygame.sprite.Sprite):
    """Снаряд (куля) танка — летить, завдає шкоди, може вибухати або рикошетити."""

    def __init__(self, pos, direction, speed=400, damage=25, color=(255, 220, 100), ricochet=False):
        super().__init__()
        self.image = pygame.Surface((8, 8), pygame.SRCALPHA)
        pygame.draw.circle(self.image, color, (4, 4), 4)
        self.rect = self.image.get_rect(center=pos)

        # Вектор руху
        self.dir = pygame.Vector2(direction).normalize()
        self.speed = speed
        self.damage = damage
        self.color = color
        self.ricochet = ricochet
        self.alive = True

        # Ефекти
        self.trail = []         # слід
        self.lifetime = 2.5     # час життя
        self.exploding = False  # чи в процесі вибуху
        self.explosion_timer = 0
        self.explosion_radius = 40

    # -----------------------------------------------------------
    def update(self, dt, blocks_group, enemies_group=None):
        """Оновлює позицію кулі та перевіряє зіткнення."""
        if not self.alive:
            return

        # рух
        move = self.dir * self.speed * dt
        self.rect.x += move.x
        self.rect.y += move.y

        # оновлення сліду
        self.trail.append(self.rect.center)
        if len(self.trail) > 15:
            self.trail.pop(0)

        # колізія з блоками
        for block in blocks_group:
            if block.rect.colliderect(self.rect):
                if block.destructible:
                    block.take_damage(self.damage)
                self._explode()
                return

        # колізія з ворогами
        if enemies_group:
            for enemy in enemies_group:
                if enemy.rect.colliderect(self.rect):
                    enemy.take_damage(self.damage)
                    self._explode()
                    return

        # межі екрана
        screen_w, screen_h = pygame.display.get_surface().get_size()
        if not (0 < self.rect.x < screen_w and 0 < self.rect.y < screen_h):
            if self.ricochet:
                self._bounce(screen_w, screen_h)
            else:
                self._explode()

        # час життя
        self.lifetime -= dt
        if self.lifetime <= 0:
            self._explode()

        # оновлення вибуху
        if self.exploding:
            self.explosion_timer -= dt
            if self.explosion_timer <= 0:
                self.kill()

    # -----------------------------------------------------------
    def _bounce(self, screen_w, screen_h):
        """Рикошет від стін."""
        if self.rect.left <= 0 or self.rect.right >= screen_w:
            self.dir.x *= -1
        if self.rect.top <= 0 or self.rect.bottom >= screen_h:
            self.dir.y *= -1
        self.rect.clamp_ip(pygame.Rect(0, 0, screen_w, screen_h))
        self.speed *= 0.8  # трохи сповільнюється
        self.lifetime -= 0.3
        print("💥 Рикошет!")

    # -----------------------------------------------------------
    def _explode(self):
        """Ініціює вибух."""
        if self.exploding:
            return
        self.exploding = True
        self.explosion_timer = 0.3
        self.speed = 0
        self.image = pygame.Surface((self.explosion_radius, self.explosion_radius), pygame.SRCALPHA)
        pygame.draw.circle(self.image, (255, 150, 50, 150),
                           (self.explosion_radius // 2, self.explosion_radius // 2),
                           self.explosion_radius // 2)
        self.rect = self.image.get_rect(center=self.rect.center)
        self.trail.clear()
        print("💣 Вибух!")

    # -----------------------------------------------------------
    def draw(self, surface):
        """Малює кулю та її слід."""
        # слід (світловий шлейф)
        for i, pos in enumerate(self.trail):
            alpha = int(200 * (i / len(self.trail)))
            trail = pygame.Surface((6, 6), pygame.SRCALPHA)
            pygame.draw.circle(trail, (*self.color, alpha), (3, 3), 3)
            surface.blit(trail, (pos[0] - 3, pos[1] - 3))

        # куля або вибух
        surface.blit(self.image, self.rect)
