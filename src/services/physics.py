"""
Низькорівневі операції: AABB-колізії, рух з урахуванням тайлів (брик/стік), проникність об’єктів (куль), ковзання по льоду.
"""

class Physics:
    def __init__(self, tilemap):
        self.tilemap = tilemap  # 2D массив тайлов

    def aabb_collision(self, rect1, rect2):
        """Проверка пересечения двух AABB"""
        return (rect1.x < rect2.x + rect2.width and
                rect1.x + rect1.width > rect2.x and
                rect1.y < rect2.y + rect2.height and
                rect1.y + rect1.height > rect2.y)

    def move(self, entity, dx, dy):
        """Движение с учетом тайлов"""
        entity.x += dx
        entity.y += dy

        # Проверка коллизий с тайлами
        for tile in self.tilemap.get_collidable_tiles(entity.rect):
            if self.aabb_collision(entity.rect, tile.rect):
                # Простая реакция на коллизию
                if dx > 0:
                    entity.x = tile.rect.x - entity.rect.width
                elif dx < 0:
                    entity.x = tile.rect.x + tile.rect.width
                if dy > 0:
                    entity.y = tile.rect.y - entity.rect.height
                elif dy < 0:
                    entity.y = tile.rect.y + tile.rect.height

    def apply_sliding(self, entity):
        """Скольжение по льду"""
        if self.tilemap.is_ice(entity.x, entity.y):
            entity.vx *= 0.95  # пример затухания скорости
            entity.vy *= 0.95
