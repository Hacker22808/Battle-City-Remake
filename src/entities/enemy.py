import pygame
import random
import math
from bullet import Bullet

class Enemy(pygame.sprite.Sprite):
    """
    Ворожий танк: рухається, стріляє, має HP, вибухає при знищенні.
    """

    def __init__(self, pos, target=None):
        super().__init__()
        self.image = pygame.Surface((40, 40), pygame.SRCALPHA)
        self.rect = self.image.get_rect(center=pos)
        self.color = (200, 60, 60)
        self._draw_tank()
        self.direction = pygame.Vector2(0, 1)
        self.speed = 80
        self.target = target
        self.hp = 100
        self.alive = True

        # Таймери
        self.shoot_cooldown = random.uniform(1.5, 3.0)
        self.change_dir_timer = random.uniform(2, 5)
        self.flash_timer = 0
        self.exploding = False
        self.explosion_timer = 0

    # -------------------------------------------------------
    def _draw_tank(self, damaged=False):
        """Малює танк."""
        surf = self.image
        surf.fill((0, 0, 0, 0))
        body_color = (200, 60, 60) if not damaged else (255, 120, 120)
        pygame.draw.rect(surf, body_color, (4, 4, 32, 32), border_radius=6)
        pygame.draw.rect(surf, (80, 0, 0), (4, 4, 32, 32), 2)
        # вежа
        pygame.draw.circle(surf, (50, 0, 0), (20, 20), 8)
        # ствол
        pygame.draw.rect(surf, (120, 0, 0), (18, 0, 4, 12))

    # -------------------------------------------------------
    def update(self, dt, blocks, bullets_group):
        """Рух, стрільба, перевірка станів."""
        if not self.alive:
            if self.exploding:
                self.explosion_timer -= dt
                if self.explosion_timer <= 0:
                    self.kill()
            return

        # Рух
        move = self.direction * self.speed * dt
        self.rect.x += move.x
        self.rect.y += move.y

        # Столкнення з блоками
        for block in blocks:
            if block.solid and block.rect.colliderect(self.rect):
                self.rect.x -= move.x
                self.rect.y -= move.y
                self._turn_random()
                break

        # Випадкова зміна напрямку
        self.change_dir_timer -= dt
        if self.change_dir_timer <= 0:
            self._turn_random()
            self.change_dir_timer = random.uniform(2, 4)

        # Стрільба
        self.shoot_cooldown -= dt
        if self.shoot_cooldown <= 0:
            self.shoot(bullets_group)
            self.shoot_cooldown = random.uniform(2.5, 5.0)

        # Візуальні ефекти
        if self.flash_timer > 0:
            self.flash_timer -= dt
            if int(self.flash_timer * 20) % 2 == 0:
                self.image.fill((255, 255, 255, 100), special_flags=pygame.BLEND_RGBA_ADD)
        else:
            self._draw_tank()

    # -------------------------------------------------------
    def _turn_random(self):
        """Змінює напрямок руху."""
        dirs = [pygame.Vector2(1, 0), pygame.Vector2(-1, 0),
                pygame.Vector2(0, 1), pygame.Vector2(0, -1)]
        self.direction = random.choice(dirs)

    # -------------------------------------------------------
    def shoot(self, bullets_group):
        """Створює кулю та додає до групи."""
        if not self.alive:
            return
        bx = self.rect.centerx + self.direction.x * 24
        by = self.rect.centery + self.direction.y * 24
        bullet = Bullet((bx, by), self.direction, speed=300, damage=20, color=(255, 140, 90))
        bullets_group.add(bullet)
        print("💥 Enemy fired a shot!")

    # -------------------------------------------------------
    def take_damage(self, dmg):
        """Отримання пошкодження."""
        self.hp -= dmg
        self.flash_timer = 0.2
        print(f"💢 Enemy hit! HP = {self.hp}")
        if self.hp <= 0:
            self.destroy()

    # -------------------------------------------------------
    def destroy(self):
        """Вибухає при знищенні."""
        self.alive = False
        self.exploding = True
        self.explosion_timer = 1.0
        boom = pygame.Surface((60, 60), pygame.SRCALPHA)
        pygame.draw.circle(boom, (255, 100, 0, 150), (30, 30), 30)
        self.image = boom
        print("💣 Enemy destroyed!")
