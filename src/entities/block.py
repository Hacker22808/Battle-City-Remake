import pygame
import random

class Block(pygame.sprite.Sprite):
    """
    Клас перешкод — блоків карти:
    brick (цегла), steel (сталь), grass (трава), ice (лід), water (вода).
    """

    def __init__(self, pos, block_type="brick"):
        super().__init__()
        self.type = block_type
        self.image = pygame.Surface((32, 32), pygame.SRCALPHA)
        self.rect = self.image.get_rect(topleft=pos)
        self.max_hp = self._define_hp()
        self.hp = self.max_hp
        self.solid = self.type not in ("grass", "water")
        self.destructible = self.type in ("brick", "ice")

        # Додаткові властивості для ефектів
        self.alpha = 255
        self.shake_timer = 0
        self._update_visual()

    # --------------------------------------------------------
    def _define_hp(self):
        """Визначає міцність блоку залежно від типу."""
        return {
            "brick": 50,
            "steel": 200,
            "grass": 10,
            "ice": 30,
            "water": 100,
        }.get(self.type, 50)

    # --------------------------------------------------------
    def _update_visual(self):
        """Малює візуальне представлення блоку."""
        surf = self.image
        surf.fill((0, 0, 0, 0))  # очищення з прозорістю

        if self.type == "brick":
            color = (180, 70, 40)
            pygame.draw.rect(surf, color, (0, 0, 32, 32))
            for y in range(0, 32, 8):
                pygame.draw.line(surf, (130, 40, 20), (0, y), (32, y), 2)
            for x in range(0, 32, 16):
                pygame.draw.line(surf, (130, 40, 20), (x, 0), (x, 32), 2)

        elif self.type == "steel":
            grad = pygame.Surface((32, 32))
            for i in range(32):
                c = 120 + int(50 * (i / 32))
                pygame.draw.line(grad, (c, c, c), (i, 0), (i, 32))
            surf.blit(grad, (0, 0))
            pygame.draw.rect(surf, (80, 80, 80), (0, 0, 32, 32), 2)

        elif self.type == "grass":
            for _ in range(40):
                x = random.randint(0, 32)
                y = random.randint(0, 32)
                pygame.draw.circle(surf, (0, random.randint(150, 255), 0), (x, y), 1)

        elif self.type == "ice":
            pygame.draw.rect(surf, (180, 230, 255), (0, 0, 32, 32))
            pygame.draw.rect(surf, (100, 180, 255), (0, 0, 32, 32), 2)

        elif self.type == "water":
            for y in range(0, 32, 8):
                color = (0, 0, 180 + y // 2)
                pygame.draw.line(surf, color, (0, y), (32, y), 2)

    # --------------------------------------------------------
    def take_damage(self, amount):
        """Отримати пошкодження (якщо блок руйнується)."""
        if not self.destructible:
            return
        self.hp -= amount
        if self.hp <= 0:
            self.destroy()
        else:
            self.shake_timer = 0.15
            self._update_visual()

    # --------------------------------------------------------
    def destroy(self):
        """Повне знищення блоку."""
        self.hp = 0
        self.alpha = 0
        self.kill()
        print(f"💥 Block {self.type} destroyed at {self.rect.topleft}")

    # --------------------------------------------------------
    def update(self, dt):
        """Оновлення стану — ефекти хитання, прозорість."""
        if self.shake_timer > 0:
            self.shake_timer -= dt
            offset = random.randint(-2, 2)
            self.rect.x += offset
            self.rect.y += offset
        elif self.hp < self.max_hp:
            # поступово повертаємося на місце
            self.rect.x = round(self.rect.x / 4) * 4
            self.rect.y = round(self.rect.y / 4) * 4

    # --------------------------------------------------------
    def draw(self, surface):
        """Відображення з урахуванням прозорості."""
        if self.alpha > 0:
            img = self.image.copy()
            img.set_alpha(self.alpha)
            surface.blit(img, self.rect)

    # --------------------------------------------------------
    def freeze(self):
        """Ефект замерзання (можна викликати для power-up)."""
        if self.type == "brick":
            self.type = "ice"
            self.destructible = True
            self.max_hp = 30
            self.hp = 30
            self._update_visual()
